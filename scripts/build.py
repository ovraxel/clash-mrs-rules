#!/usr/bin/env python3
"""Build Mihomo domain/ipcidr MRS files from remote YAML/TXT or local TXT/YAML."""
import hashlib
import ipaddress
import json
import os
import re
import shutil
import subprocess
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / 'config' / 'sources.json'
OUTPUT = ROOT / 'output'
TEMP = ROOT / '.build'
PUBLISH = ROOT / 'rule' / 'Clash'
MANIFEST = '.mrs-managed.json'
REPO = os.environ.get('GITHUB_REPOSITORY', 'wiedergeburtme/clash-mrs-rules')
BRANCH = os.environ.get('GITHUB_REF_NAME', 'main')
CACHE = {}
NAME_RE = re.compile(r'[A-Za-z0-9_-]+\Z')
DOMAIN_LABEL = re.compile(r'[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?\Z', re.I)


def valid_domain(value):
    return bool(value and len(value) <= 253 and all(DOMAIN_LABEL.fullmatch(label) for label in value.split('.')))


def valid_keyword(value):
    return bool(value and len(value) <= 253 and not any(ch.isspace() for ch in value) and ',' not in value)


def load_config():
    with CONFIG.open(encoding='utf-8') as stream:
        rules = json.load(stream).get('rules')
    if not isinstance(rules, list) or not rules:
        raise ValueError('config/sources.json: rules must be a nonempty list')
    seen = set()
    for rule in rules:
        if not isinstance(rule, dict):
            raise ValueError('Each rule must be an object')
        name = rule.get('name')
        behavior = rule.get('behavior')
        fmt = rule.get('format', 'classical')
        minimum = rule.get('min_rules', 1)
        if not isinstance(name, str) or not NAME_RE.fullmatch(name) or name in seen:
            raise ValueError(f'Invalid or duplicate rule name: {name}')
        seen.add(name)
        if behavior not in ('domain', 'ipcidr'):
            raise ValueError(f'{name}: behavior must be domain or ipcidr')
        if fmt not in ('classical', 'domain', 'ipcidr', 'text', 'yaml'):
            raise ValueError(f'{name}: unsupported format {fmt}')
        if fmt == 'domain' and behavior != 'domain' or fmt == 'ipcidr' and behavior != 'ipcidr':
            raise ValueError(f'{name}: source format and behavior disagree')
        if type(minimum) is not int or minimum < 1:
            raise ValueError(f'{name}: min_rules must be a positive integer')
        validate_source(rule, name)
        extras = rule.get('extra_urls', [])
        if not isinstance(extras, list):
            raise ValueError(f'{name}: extra_urls must be a list')
        for extra in extras:
            if not isinstance(extra, dict) or extra.get('format') not in ('classical', 'domain', 'ipcidr', 'text', 'yaml'):
                raise ValueError(f'{name}: invalid extra source')
            if extra['format'] == 'domain' and behavior != 'domain' or extra['format'] == 'ipcidr' and behavior != 'ipcidr':
                raise ValueError(f'{name}: extra source format and behavior disagree')
            validate_source(extra, name)
    return rules


def validate_source(item, name):
    url, filename = item.get('url'), item.get('file')
    if (url is None) == (filename is None):
        raise ValueError(f'{name}: specify exactly one of url or file')
    if url is not None and (not isinstance(url, str) or not url.startswith('https://')):
        raise ValueError(f'{name}: URL must use HTTPS')
    if filename is not None and (not isinstance(filename, str) or not filename.strip()):
        raise ValueError(f'{name}: invalid local file path')
    if filename is not None:
        local_path(filename)  # validate traversal before build


def local_path(filename):
    path = (ROOT / filename).resolve()
    if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
        raise ValueError(f'Unsafe or missing local source: {filename}')
    return path


def read_source(item):
    if item.get('file') is not None:
        return local_path(item['file']).read_text(encoding='utf-8-sig')
    url = item['url']
    if url not in CACHE:
        print(f'Downloading {url}', flush=True)
        req = urllib.request.Request(url, headers={'User-Agent': 'clash-mrs-rules/3.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read(20 * 1024 * 1024 + 1)
        if len(data) > 20 * 1024 * 1024:
            raise RuntimeError(f'Source larger than 20 MB: {url}')
        CACHE[url] = data.decode('utf-8-sig')
    return CACHE[url]


def parse_source(content, fmt):
    if fmt == 'text':
        return content.splitlines()
    parsed = yaml.safe_load(content)
    if not isinstance(parsed, dict) or not isinstance(parsed.get('payload'), list):
        raise ValueError('YAML source must contain a payload list')
    payload = parsed['payload']
    if not all(isinstance(line, str) for line in payload):
        raise ValueError('YAML payload entries must be strings')
    return payload


def normalize_domain(raw, fmt):
    line = raw.strip().strip("'\"").strip()
    if not line or line.startswith('#'):
        return None
    if fmt in ('classical', 'yaml'):
        parts = [part.strip() for part in line.split(',')]
        if len(parts) < 2:
            return None
        kind, value = parts[0].upper(), parts[1].lower()
        if kind == 'DOMAIN' and valid_domain(value):
            return 'full:' + value
        if kind == 'DOMAIN-SUFFIX' and valid_domain(value):
            return '+.' + value
        if kind == 'DOMAIN-KEYWORD' and valid_keyword(value):
            return 'keyword:' + value
        return None
    line = line.lower()
    if line.startswith('full:'):
        return line if valid_domain(line[5:]) else None
    if line.startswith('keyword:'):
        return line if valid_keyword(line[8:]) else None
    if line.startswith(('+.', '*.')):
        return line if valid_domain(line[2:]) else None
    if line.startswith('.'):
        return '+.' + line[1:] if valid_domain(line[1:]) else None
    return line if valid_domain(line) else None


def normalize_ip(raw, fmt):
    line = raw.strip().strip("'\"").strip()
    if not line or line.startswith('#'):
        return None
    if fmt in ('classical', 'yaml'):
        parts = [part.strip() for part in line.split(',')]
        if len(parts) < 2 or parts[0].upper() not in ('IP-CIDR', 'IP-CIDR6'):
            return None
        line = parts[1]
    elif ',' in line:
        return None
    try:
        return str(ipaddress.ip_network(line, strict=False))
    except ValueError:
        return None


def source_reference(item):
    if item.get('file') is not None:
        return f"https://github.com/{REPO}/blob/{BRANCH}/{item['file']}"
    return item['url']


def generate_readme(rule, count):
    name, behavior = rule['name'], rule['behavior']
    raw = f'https://raw.githubusercontent.com/{REPO}/{BRANCH}/rule/Clash/{name}/{name}.mrs'
    cdn = f'https://cdn.jsdelivr.net/gh/{REPO}@{BRANCH}/rule/Clash/{name}/{name}.mrs'
    sources = [rule] + rule.get('extra_urls', [])
    refs = '\n'.join(f'- <{source_reference(item)}>' for item in sources)
    note = ('\n> Classical 來源只提取與本 MRS behavior 相容的規則；不支援的類型不會轉入。\n'
            if any(item.get('format', 'classical') in ('classical', 'yaml') for item in sources) else '')
    return f'''# {name} MRS 規則

由 GitHub Actions 自動生成，適用於 Mihomo。

## GitHub Raw（使用程式碼區塊右上角按鈕複製）

```text
{raw}
```

[開啟／下載 MRS]({raw})

## jsDelivr CDN

```text
{cdn}
```

[開啟 CDN 地址]({cdn})

## 規則資訊

| 項目 | 內容 |
|---|---|
| 名稱 | {name} |
| Behavior | {behavior} |
| 去重後規則數 | {count} |
| 更新頻率 | 每日 |
{note}
## Mihomo 配置

```yaml
rule-providers:
  {name}:
    type: http
    behavior: {behavior}
    format: mrs
    url: "{raw}"
    path: ./ruleset/{name}.mrs
    interval: 86400
```

## 來源

{refs}

---

此 README 由 GitHub Actions 自動生成。
'''


def build_rule(rule, stage):
    name, behavior = rule['name'], rule['behavior']
    sources = [rule] + rule.get('extra_urls', [])
    converted = set()
    skipped = 0
    for item in sources:
        fmt = item.get('format', 'classical')
        payload = parse_source(read_source(item), fmt)
        valid = 0
        for raw in payload:
            value = normalize_domain(raw, fmt) if behavior == 'domain' else normalize_ip(raw, fmt)
            if value is not None:
                converted.add(value)
                valid += 1
            elif raw.strip() and not raw.lstrip().startswith('#'):
                skipped += 1
        print(f'{name}: {source_reference(item)}: recognized={valid}', flush=True)
    if len(converted) < rule.get('min_rules', 1):
        raise RuntimeError(f'{name}: only {len(converted)} valid rules')
    source = TEMP / f'{name}.txt'
    target = OUTPUT / f'{name}.mrs'
    source.write_text('\n'.join(sorted(converted)) + '\n', encoding='utf-8')
    subprocess.run(['mihomo', 'convert-ruleset', behavior, 'text', str(source), str(target)], check=True)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f'{name}: missing or empty MRS')
    folder = stage / name
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(target, folder / target.name)
    (folder / 'README.md').write_text(generate_readme(rule, len(converted)), encoding='utf-8')
    print(f'{name}: unique={len(converted)}, unconverted/other-behavior={skipped}, bytes={target.stat().st_size}', flush=True)


def generate_checksums(stage):
    files = sorted(OUTPUT.glob('*.mrs'))
    if not files:
        raise RuntimeError('No MRS files generated')
    lines = [f'{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}' for path in files]
    contents = '\n'.join(lines) + '\n'
    (OUTPUT / 'SHA256SUMS').write_text(contents, encoding='utf-8')
    (stage / 'SHA256SUMS').write_text(contents, encoding='utf-8')
    subprocess.run(['sha256sum', '-c', 'SHA256SUMS'], cwd=OUTPUT, check=True)


def publish(stage, rules):
    PUBLISH.mkdir(parents=True, exist_ok=True)
    manifest_path = PUBLISH / MANIFEST
    previous = []
    if manifest_path.exists():
        previous = json.loads(manifest_path.read_text(encoding='utf-8')).get('managed_rules', [])
        if not isinstance(previous, list) or any(not isinstance(n, str) or not NAME_RE.fullmatch(n) for n in previous):
            raise ValueError('Invalid managed rules manifest')
    current = [rule['name'] for rule in rules]
    for name in previous:
        if name not in current and (PUBLISH / name).is_dir():
            shutil.rmtree(PUBLISH / name)
    for name in current:
        destination = PUBLISH / name
        destination.mkdir(parents=True, exist_ok=True)
        for filename in (f'{name}.mrs', 'README.md'):
            shutil.copyfile(stage / name / filename, destination / filename)
    shutil.copyfile(stage / 'SHA256SUMS', PUBLISH / 'SHA256SUMS')
    manifest_path.write_text(json.dumps({'managed_rules': sorted(current)}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    rules = load_config()
    for folder in (OUTPUT, TEMP):
        if folder.exists():
            shutil.rmtree(folder)
        folder.mkdir(parents=True)
    stage = TEMP / 'publish'
    stage.mkdir(parents=True)
    for rule in rules:
        build_rule(rule, stage)
    generate_checksums(stage)
    publish(stage, rules)
    print('All MRS files built and published successfully.', flush=True)


if __name__ == '__main__':
    main()
