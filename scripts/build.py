#!/usr/bin/env python3
"""Build Mihomo MRS files exclusively from local domain/IP TXT sources."""
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / 'sources'
DEST = ROOT / 'rule' / 'Clash'
STAGE = ROOT / '.build' / 'publish'
REPO = os.environ.get('GITHUB_REPOSITORY', 'wiedergeburtme/clash-mrs-rules')
BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')
MANIFEST = DEST / '.mrs-managed.json'
NAME_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9_-]*\Z')
LABEL_RE = re.compile(r'[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?\Z', re.I)


def valid_domain(s):
    if not s or len(s) > 253 or any(not LABEL_RE.fullmatch(p) for p in s.split('.')):
        return False
    return True


def domain_line(line):
    value = line.lower()
    if value.startswith('full:'):
        return value if valid_domain(value[5:]) else None
    if value.startswith('keyword:'):
        word = value[8:]
        return value if word and len(word) <= 253 and not any(c.isspace() or c == ',' for c in word) else None
    if value.startswith('*.'):
        return value if valid_domain(value[2:]) else None
    if value.startswith('+.'):
        return value if valid_domain(value[2:]) else None
    if value.startswith('.'):
        return '+.' + value[1:] if valid_domain(value[1:]) else None
    return value if valid_domain(value) else None


def ip_line(line):
    if ',' in line or ' ' in line:
        return None
    try:
        return str(ipaddress.ip_network(line, strict=False))
    except ValueError:
        return None


def read_lines(path, behavior):
    result = set()
    raw_count = 0
    for number, original in enumerate(path.read_text(encoding='utf-8-sig').splitlines(), 1):
        line = original.strip()
        if not line or line.startswith('#'):
            continue
        raw_count += 1
        value = domain_line(line) if behavior == 'domain' else ip_line(line)
        if value is None:
            raise ValueError(f'{path.relative_to(ROOT)}:{number}: invalid {behavior} rule: {line!r}')
        result.add(value)
    if not result:
        raise ValueError(f'{path.relative_to(ROOT)}: no rules; delete empty TXT instead')
    return sorted(result), raw_count


def readme(name, behavior, count, source):
    base = f'rule/Clash/{name}/{name}.mrs'
    raw = f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/{base}'
    cdn = f'https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/{base}'
    source_url = f'https://github.com/{REPO}/blob/{BRANCH}/{source.as_posix()}'
    return f'''# {name} MRS\n\n由本倉庫 TXT 規則自動轉換；Behavior：`{behavior}`；去重後規則數：**{count}**。\n\n## GitHub Raw（可用程式碼區塊右上角複製）\n\n```text\n{raw}\n```\n\n[開啟／下載 MRS]({raw})\n\n## jsDelivr CDN\n\n```text\n{cdn}\n```\n\n## Mihomo 配置\n\n```yaml\nrule-providers:\n  {name}:\n    type: http\n    behavior: {behavior}\n    format: mrs\n    url: "{raw}"\n    path: ./ruleset/{name}.mrs\n    interval: 86400\n```\n\n## TXT 來源\n\n[{source.as_posix()}]({source_url})\n'''


def main():
    if not re.fullmatch(r'[\w.-]+/[\w.-]+', REPO):
        raise ValueError('Invalid GITHUB_REPOSITORY')
    if not re.fullmatch(r'[A-Za-z0-9._/-]+', BRANCH):
        raise ValueError('Invalid GITHUB_REF_NAME')
    if STAGE.parent.exists():
        shutil.rmtree(STAGE.parent)
    STAGE.mkdir(parents=True)
    entries = []
    names = set()
    for folder, behavior in ((SOURCES / 'domain', 'domain'), (SOURCES / 'ip', 'ipcidr')):
        if not folder.exists():
            continue
        for source in sorted(folder.glob('*.txt')):
            name = source.stem
            if not NAME_RE.fullmatch(name):
                raise ValueError(f'Invalid TXT filename: {source.name}')
            if name.casefold() in names:
                raise ValueError(f'Duplicate output name across domain/ip: {name}')
            names.add(name.casefold())
            entries.append((source, name, behavior))
    if not entries:
        raise ValueError('No TXT found under sources/domain or sources/ip')
    checksums = []
    for source, name, behavior in entries:
        lines, original = read_lines(source, behavior)
        folder = STAGE / name
        folder.mkdir()
        input_txt = STAGE.parent / f'{name}.txt'
        input_txt.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        output = folder / f'{name}.mrs'
        subprocess.run(['mihomo', 'convert-ruleset', behavior, 'text', str(input_txt), str(output)], check=True)
        if not output.is_file() or not output.stat().st_size:
            raise RuntimeError(f'{name}: empty or missing MRS')
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        checksums.append(f'{digest}  {name}/{name}.mrs')
        (folder / 'README.md').write_text(readme(name, behavior, len(lines), source.relative_to(ROOT)), encoding='utf-8')
        print(f'{name}: {behavior}; input={original}; unique={len(lines)}; sha256={digest}', flush=True)
    (STAGE / 'SHA256SUMS').write_text('\n'.join(checksums) + '\n', encoding='utf-8')
    # Check every staged binary before touching published content.
    for entry in checksums:
        digest, relative = entry.split('  ', 1)
        actual = hashlib.sha256((STAGE / relative).read_bytes()).hexdigest()
        if actual != digest:
            raise RuntimeError(f'Checksum mismatch: {relative}')
    DEST.mkdir(parents=True, exist_ok=True)
    # A deliberate migration: only remove directories previously recorded as managed.
    previous = []
    if MANIFEST.exists():
        data = json.loads(MANIFEST.read_text(encoding='utf-8'))
        previous = data.get('managed_rules', [])
        if not isinstance(previous, list) or any(not isinstance(n, str) or not NAME_RE.fullmatch(n) for n in previous):
            raise ValueError('Unsafe existing manifest; stop without deleting anything')
    current = [name for _, name, _ in entries]
    for name in previous:
        if name not in current and (DEST / name).is_dir():
            shutil.rmtree(DEST / name)
    for name in current:
        target = DEST / name
        target.mkdir(exist_ok=True)
        for filename in (f'{name}.mrs', 'README.md'):
            shutil.copyfile(STAGE / name / filename, target / filename)
    shutil.copyfile(STAGE / 'SHA256SUMS', DEST / 'SHA256SUMS')
    MANIFEST.write_text(json.dumps({'managed_rules': current}, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'Successfully published {len(current)} MRS files.', flush=True)


if __name__ == '__main__':
    main()
