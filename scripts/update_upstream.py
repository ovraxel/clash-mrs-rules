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
from shadowrocket_rules import render

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'config/upstream.json'
DEST = ROOT / 'rule/Upstream'
STAGE = ROOT / '.build-upstream'
SHADOW_DEST = ROOT / 'rule' / 'Shadowrocket' / 'Upstream'
SHADOW_STAGE = ROOT / '.build-upstream-shadowrocket'
SHADOW_MANIFEST = SHADOW_DEST / '.list-managed.json'
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

def fetch(url):
    if not url.startswith('https://raw.githubusercontent.com/'):
        raise ValueError(f'Unapproved source URL: {url}')
    req = urllib.request.Request(url, headers={'User-Agent': 'clash-mrs-rules-upstream/2.0'})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read(20 * 1024 * 1024 + 1)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(f'WARNING: HTTP 404; skipping source: {url}', flush=True)
            return None
        raise RuntimeError(f'HTTP {exc.code} fetching {url}') from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f'Network error fetching {url}: {exc.reason}') from exc
    if len(raw) > 20 * 1024 * 1024:
        raise ValueError(f'Source too large: {url}')
    return raw.decode('utf-8-sig')

def parse_mihomo(content, behavior):
    result = set()
    for n, raw in enumerate(content.splitlines(), 1):
        line = raw.strip().lstrip('\ufeff')
        if not line or line.startswith('#'):
            continue
        line = line.split(' #', 1)[0].strip()
        if behavior == 'domain':
            if line.startswith('+.'):
                result.add('+.' + domain(line[2:]))
            elif line.startswith('full:'):
                result.add('full:' + domain(line[5:]))
            elif line.startswith('keyword:'):
                value = line[8:].lower()
                if not value or any(c.isspace() for c in value):
                    raise ValueError(f'Invalid keyword at line {n}')
                result.add('keyword:' + value)
            elif line.startswith('.'):
                result.add('+.' + domain(line[1:]))
            else:
                result.add('+.' + domain(line))
        else:
            result.add(str(ipaddress.ip_network(line, strict=False)))
    return result

def parse_geosite(content, url, visited, depth=0):
    if depth > 12:
        raise ValueError('Geosite include depth exceeded')
    result, ignored = set(), []
    for n, raw in enumerate(content.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        line = line.split(' @', 1)[0].split(' #', 1)[0].strip()
        if not line:
            continue
        if line.startswith('include:'):
            target = line[8:].strip()
            # Geosite supports attribute-filtered includes, e.g. include:bytedance-ai-!cn.
            # Filtering requires retaining per-entry attributes; never silently include
            # the entire child category, as that changes the meaning of the rule.
            if not re.fullmatch(r'[A-Za-z0-9_.-]+', target):
                ignored.append(f'{n}: unsupported attribute-filtered include: {line}')
                continue
            child = url.rsplit('/', 1)[0] + '/' + target
            if child in visited:
                continue
            visited.add(child)
            raw_child = fetch(child)
            if raw_child is None:
                raise RuntimeError(f'Missing Geosite include: {child}')
            extra, extra_ignored = parse_geosite(raw_child, child, visited, depth + 1)
            result.update(extra)
            ignored.extend(extra_ignored)
        elif line.startswith('regexp:'):
            ignored.append(f'{n}: unsupported regexp: {line}')
        elif line.startswith('domain:'):
            result.add('+.' + domain(line[7:]))
        elif line.startswith('full:'):
            result.add('full:' + domain(line[5:]))
        elif line.startswith('keyword:'):
            value = line[8:].lower()
            if not value or any(c.isspace() for c in value):
                raise ValueError(f'Invalid Geosite keyword: {line}')
            result.add('keyword:' + value)
        else:
            result.add('+.' + domain(line))
    return result, ignored

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
    if SHADOW_STAGE.exists():
        shutil.rmtree(SHADOW_STAGE)
    SHADOW_STAGE.mkdir(parents=True)
    outputs, used, missing_sources = [], set(), set()
    for rule in rules:
        provider, name = rule['provider'], rule['name']
        if not NAME.fullmatch(provider) or not NAME.fullmatch(name) or (provider.casefold(), name.casefold()) in used:
            raise ValueError('Invalid or duplicate provider/name')
        used.add((provider.casefold(), name.casefold()))
        sources = rule.get('sources')
        if sources is None:
            sources = [{'provider': provider, 'format': rule['format'], 'url': rule['url']}]
        if not isinstance(sources, list) or not sources:
            raise ValueError(f'{provider}/{name}: sources must be nonempty list')
        combined = {'domain': set(), 'ipcidr': set()}
        ignored, successful, source_details = [], 0, []
        for item in sources:
            url, fmt = item['url'], item['format']
            if fmt not in ('classical-list', 'mihomo-domain', 'mihomo-ipcidr', 'geosite'):
                raise ValueError(f'Unsupported format: {fmt}')
            raw = fetch(url)
            if raw is None:
                continue
            if fmt == 'classical-list':
                parsed, skipped = parse(raw)
                for behavior in combined:
                    combined[behavior].update(parsed[behavior])
            elif fmt == 'geosite':
                parsed_domain, skipped = parse_geosite(raw, url, {url})
                combined['domain'].update(parsed_domain)
            else:
                behavior = 'domain' if fmt == 'mihomo-domain' else 'ipcidr'
                combined[behavior].update(parse_mihomo(raw, behavior))
                skipped = []
            successful += 1
            ignored.extend(f'{url}: {x}' for x in skipped)
            source_details.append(url)
            print(f'{provider}/{name}: source {fmt} loaded: {url}', flush=True)
        if not successful:
            print(f'WARNING: {provider}/{name}: all sources returned 404; preserving previous output', flush=True)
            missing_sources.add((provider, name))
            continue
        if ignored:
            print(f'{provider}/{name}: unsupported entries skipped ({len(ignored)}): {ignored[:30]}', flush=True)
        for behavior, enabled, suffix in (('domain', rule.get('domain', False), ''), ('ipcidr', rule.get('ipcidr', False), '-IP')):
            if not isinstance(enabled, bool):
                raise ValueError('domain/ipcidr must be booleans')
            if not enabled:
                continue
            lines = sorted(combined[behavior])
            if not lines:
                print(f'{provider}/{name}: no {behavior} rules; skipping empty output', flush=True)
                continue
            outname = name + suffix
            folder = STAGE / provider / outname
            folder.mkdir(parents=True)
            shadow_folder = SHADOW_STAGE / provider / outname
            shadow_folder.mkdir(parents=True)
            (shadow_folder / f'{outname}.list').write_text(render(lines, behavior), encoding='utf-8')
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
            provenance = '\n'.join(f'- {u}' for u in source_details)
            readme = (f'# {outname}\n\nSources ({successful}):\n{provenance}\n\n'
                      f'Behavior: `{behavior}`; unique rules: {len(lines)}.\n\n'
                      f'Unsupported entries skipped: {len(ignored)}.\n\n'
                      f'## Raw\n\n```text\n{rawurl}\n```\n\n'
                      f'## CDN\n\n```text\n{cdn}\n```\n\n'
                      f'## Mihomo\n\n```yaml\n{outname}:\n    type: http\n'
                      f'    behavior: {behavior}\n    format: mrs\n    interval: 86400\n'
                      f'    url: {rawurl}\n```\n')
            (folder / 'README.md').write_text(readme, encoding='utf-8')
            outputs.append((relative, hashlib.sha256(binary.read_bytes()).hexdigest()))
            print(f'{relative}: {len(lines)} unique rules from {successful} sources', flush=True)
    # Preserve previously published files when a configured source temporarily returns 404.
    manifest = DEST / '.mrs-managed.json'
    previous = []
    if manifest.exists():
        previous = json.loads(manifest.read_text(encoding='utf-8')).get('managed_rules', [])
        if not isinstance(previous, list) or any(not isinstance(x, str) or len(x.split('/')) != 2 or not all(NAME.fullmatch(p) for p in x.split('/')) for x in previous):
            raise ValueError('Unsafe upstream manifest')
    preserved = [old for old in previous if (old.split('/')[0], old.split('/')[1].removesuffix('-IP')) in missing_sources]
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
    # Keep previously published LIST when an upstream temporarily returns 404.
    SHADOW_DEST.mkdir(parents=True, exist_ok=True)
    shadow_previous = []
    if SHADOW_MANIFEST.exists():
        shadow_previous = json.loads(SHADOW_MANIFEST.read_text(encoding='utf-8')).get('managed_rules', [])
        if not isinstance(shadow_previous, list) or any(not isinstance(x, str) or len(x.split('/')) != 2 or not all(NAME.fullmatch(p) for p in x.split('/')) for x in shadow_previous):
            raise ValueError('Unsafe Shadowrocket upstream manifest')
    shadow_current = []
    for old in current:
        if (SHADOW_STAGE / old / (Path(old).name + '.list')).exists():
            shadow_current.append(old)
        elif old in shadow_previous and (SHADOW_DEST / old / (Path(old).name + '.list')).exists():
            shadow_current.append(old)
    for old in shadow_previous:
        if old not in shadow_current and (SHADOW_DEST / old).is_dir():
            shutil.rmtree(SHADOW_DEST / old)
    for old in shadow_current:
        source_list = SHADOW_STAGE / old / (Path(old).name + '.list')
        if source_list.exists():
            target = SHADOW_DEST / old
            target.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_list, target / source_list.name)
    SHADOW_MANIFEST.write_text(json.dumps({'managed_rules': shadow_current}, indent=2) + '\n', encoding='utf-8')
    print(f'Shadowrocket upstream LIST published: {len(shadow_current)}', flush=True)
    print(f'Upstream build completed: {len(outputs)} MRS files; {len(missing_sources)} missing sources skipped', flush=True)

if __name__ == '__main__':
    main()
