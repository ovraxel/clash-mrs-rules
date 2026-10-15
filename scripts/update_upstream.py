#!/usr/bin/env python3
"""Build separate upstream MRS; never reads/writes manual TXT or rule/Clash."""
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'config/upstream.json'
DEST = ROOT / 'rule/Upstream'
STAGE = ROOT / '.build-upstream'
REPO = os.environ.get('GITHUB_REPOSITORY', 'wiedergeburtme/clash-mrs-rules')
BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')
NAME = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]*\Z')
LABEL = re.compile(r'[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?\Z', re.I)

def domain(value):
    value = value.lower().strip()
    if not value or len(value) > 253 or not all(LABEL.fullmatch(x) for x in value.split('.')):
        raise ValueError(f'Invalid domain: {value}')
    return value

def parse(content):
    domains, ips, ignored = set(), set(), []
    for number, raw in enumerate(content.splitlines(), 1):
        line = raw.strip().lstrip('\ufeff')
        if not line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split(',')]
        kind = parts[0].upper()
        if kind in ('DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6'):
            if len(parts) < 2 or not parts[1]:
                raise ValueError(f'Line {number}: malformed {line}')
            value = parts[1]
            if kind == 'DOMAIN':
                domains.add('full:' + domain(value))
            elif kind == 'DOMAIN-SUFFIX':
                domains.add('+.' + domain(value))
            elif kind == 'DOMAIN-KEYWORD':
                if any(c.isspace() for c in value) or not value or len(value) > 253:
                    raise ValueError(f'Line {number}: invalid keyword')
                domains.add('keyword:' + value.lower())
            else:
                network = ipaddress.ip_network(value, strict=False)
                if (kind == 'IP-CIDR' and network.version != 4) or (kind == 'IP-CIDR6' and network.version != 6):
                    raise ValueError(f'Line {number}: mismatched IP version')
                ips.add(str(network))
        elif kind in ('PROCESS-NAME', 'PROCESS-PATH', 'PROCESS-NAME-REGEX', 'IP-ASN'):
            ignored.append(f'{number}: {line}')
        else:
            raise ValueError(f'Line {number}: unsupported rule: {line}')
    return {'domain': sorted(domains), 'ipcidr': sorted(ips)}, ignored

def main():
    data = json.loads(CONFIG.read_text(encoding='utf-8'))
    rules = data.get('rules')
    if not isinstance(rules, list) or not rules:
        raise ValueError('upstream.json rules must be nonempty list')
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', REPO) or not re.fullmatch(r'[A-Za-z0-9._/-]+', BRANCH):
        raise ValueError('Invalid repository or branch')
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    outputs, used = [], set()
    missing_sources = set()
    for rule in rules:
        provider, name, url = rule['provider'], rule['name'], rule['url']
        if not NAME.fullmatch(provider) or not NAME.fullmatch(name) or (provider.casefold(), name.casefold()) in used:
            raise ValueError('Invalid or duplicate provider/name')
        used.add((provider.casefold(), name.casefold()))
        if rule.get('format') != 'classical-list' or not url.startswith('https://raw.githubusercontent.com/'):
            raise ValueError('Only HTTPS raw classical-list source supported')
        req = urllib.request.Request(url, headers={'User-Agent': 'clash-mrs-rules-upstream/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read(20 * 1024 * 1024 + 1)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                print(f'WARNING: {provider}/{name}: source returned HTTP 404; skipping: {url}', flush=True)
                missing_sources.add((provider, name))
                continue
            raise RuntimeError(f'{provider}/{name}: HTTP {exc.code} fetching {url}') from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f'{provider}/{name}: network error fetching {url}: {exc.reason}') from exc
        if len(raw) > 20 * 1024 * 1024:
            raise ValueError('Upstream source too large')
        parsed, ignored = parse(raw.decode('utf-8-sig'))
        if ignored:
            print(f'{provider}/{name}: rules not representable as domain/ipcidr MRS ignored: {ignored}', flush=True)
        for behavior, enabled, suffix in (('domain', rule.get('domain', False), ''), ('ipcidr', rule.get('ipcidr', False), '-IP')):
            if not isinstance(enabled, bool):
                raise ValueError('domain/ipcidr must be booleans')
            if not enabled:
                continue
            lines = parsed[behavior]
            if not lines:
                print(f'{provider}/{name}: no {behavior} rules; skipping empty output', flush=True)
                continue
            outname = name + suffix
            folder = STAGE / provider / outname
            folder.mkdir(parents=True)
            source = folder / 'input.txt'
            source.write_text('\n'.join(lines) + '\n', encoding='utf-8')
            binary = folder / (outname + '.mrs')
            subprocess.run(['mihomo', 'convert-ruleset', behavior, 'text', str(source), str(binary)], check=True)
            if not binary.is_file() or not binary.stat().st_size:
                raise RuntimeError(f'{outname}: missing MRS')
            source.unlink()
            relative = f'{provider}/{outname}/{outname}.mrs'
            rawurl = f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/rule/Upstream/{relative}'
            cdn = f'https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/rule/Upstream/{relative}'
            (folder / 'README.md').write_text(f'# {outname}\n\nUpstream: [{provider}]({url})\n\nBehavior: `{behavior}`; unique rules: {len(lines)}.\n\nNon-domain/IP rules omitted: {len(ignored)}.\n\n## Raw\n\n```text\n{rawurl}\n```\n\n## CDN\n\n```text\n{cdn}\n```\n\n## Mihomo\n\n```yaml\n{outname}:\n    type: http\n    behavior: {behavior}\n    format: mrs\n    interval: 86400\n    url: {rawurl}\n```\n', encoding='utf-8')
            outputs.append((relative, hashlib.sha256(binary.read_bytes()).hexdigest()))
            print(f'{relative}: {len(lines)} rules', flush=True)
    # Preserve previously published files when a configured source temporarily returns 404.
    manifest = DEST / '.mrs-managed.json'
    previous = []
    if manifest.exists():
        previous = json.loads(manifest.read_text(encoding='utf-8')).get('managed_rules', [])
        if not isinstance(previous, list) or any(not isinstance(x, str) or len(x.split('/')) != 2 or not all(NAME.fullmatch(p) for p in x.split('/')) for x in previous):
            raise ValueError('Unsafe upstream manifest')
    preserved = [old for old in previous if tuple(old.split('/')[0:1] + [old.split('/')[1].removesuffix('-IP')]) in missing_sources]
    for old in preserved:
        folder = DEST / old
        for binary in folder.glob('*.mrs'):
            rel = f'{old}/{binary.name}'
            outputs.append((rel, hashlib.sha256(binary.read_bytes()).hexdigest()))
    (STAGE / 'SHA256SUMS').write_text(''.join(f'{digest}  {path}\n' for path, digest in outputs), encoding='utf-8')
    for path, digest in outputs:
        if hashlib.sha256(((STAGE / path) if (STAGE / path).exists() else (DEST / path)).read_bytes()).hexdigest() != digest:
            raise RuntimeError(f'Checksum mismatch: {path}')
    # Only after all sources and binaries succeed, update managed upstream files.
    DEST.mkdir(parents=True, exist_ok=True)
    current = [str(Path(path).parent) for path, _ in outputs]
    for old in previous:
        if old not in current and (DEST / old).is_dir():
            shutil.rmtree(DEST / old)
    for old in current:
        target = DEST / old
        target.mkdir(parents=True, exist_ok=True)
        if (STAGE / old).exists():
            for src in (STAGE / old).iterdir():
                shutil.copyfile(src, target / src.name)
    shutil.copyfile(STAGE / 'SHA256SUMS', DEST / 'SHA256SUMS')
    manifest.write_text(json.dumps({'managed_rules': current}, indent=2) + '\n', encoding='utf-8')
    print(f'Upstream build completed: {len(outputs)} MRS files; {len(missing_sources)} missing sources skipped', flush=True)

if __name__ == '__main__':
    main()
