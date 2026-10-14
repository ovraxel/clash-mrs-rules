
#!/usr/bin/env python3

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


# ==========================================
# 1. Project paths
# ==========================================

ROOT = Path(__file__).resolve().parent.parent

CONFIG = ROOT / "config" / "sources.json"
OUTPUT = ROOT / "output"
TEMP = ROOT / ".build"
PUBLISH = ROOT / "rule" / "Clash"

MANIFEST = ".mrs-managed.json"

REPO = os.environ.get("GITHUB_REPOSITORY", "")
BRANCH = os.environ.get("GITHUB_REF_NAME", "main")

if not re.fullmatch(r"[\w.-]+/[\w.-]+", REPO):
    raise RuntimeError(
        "GITHUB_REPOSITORY is missing or invalid"
    )

if not re.fullmatch(r"[A-Za-z0-9._/-]+", BRANCH):
    raise RuntimeError("Invalid branch name")


# ==========================================
# 2. Load configuration
# ==========================================

def load_config():

    with CONFIG.open(encoding="utf-8") as f:
        data = json.load(f)

    rules = data.get("rules")

    if not isinstance(rules, list) or not rules:
        raise ValueError("No rules configured")

    seen = set()

    for rule in rules:

        if not isinstance(rule, dict):
            raise ValueError("Invalid rule configuration")

        name = rule.get("name")
        behavior = rule.get("behavior")
        source_format = rule.get("format", "classical")
        url = rule.get("url")
        minimum = rule.get("min_rules", 1)

        if not isinstance(name, str) or not re.fullmatch(
            r"[A-Za-z0-9_-]+", name
        ):
            raise ValueError(f"Invalid rule name: {name}")

        if name in seen:
            raise ValueError(f"Duplicate rule name: {name}")

        seen.add(name)

        if behavior not in ("domain", "ipcidr"):
            raise ValueError(
                f"{name}: Unsupported MRS behavior"
            )

        if source_format not in (
            "classical",
            "domain",
            "ipcidr",
            "text"
        ):
            raise ValueError(
                f"{name}: Unsupported source format"
            )

        if not isinstance(url, str) or not url.startswith(
            "https://"
        ):
            raise ValueError(f"{name}: Invalid HTTPS URL")

        if type(minimum) is not int or minimum < 1:
            raise ValueError(
                f"{name}: min_rules must be >= 1"
            )

    return rules


# ==========================================
# 3. Download upstream sources
# ==========================================

CACHE = {}


def download(url):

    if url in CACHE:
        return CACHE[url]

    print(f"Downloading: {url}", flush=True)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Clash-MRS-Builder/2.1"
        }
    )

    with urllib.request.urlopen(
        request,
        timeout=60
    ) as response:

        content = response.read(20 * 1024 * 1024 + 1)

    if len(content) > 20 * 1024 * 1024:
        raise RuntimeError("Source exceeds 20 MB")

    text = content.decode("utf-8-sig")

    CACHE[url] = text

    return text


# ==========================================
# 4. Parse YAML / TXT
# ==========================================

def parse_source(content, source_format):

    if source_format == "text":
        return content.splitlines()

    data = yaml.safe_load(content)

    if not isinstance(data, dict):
        raise ValueError("Expected a YAML mapping")

    payload = data.get("payload")

    if not isinstance(payload, list) or not payload:
        raise ValueError("Missing or empty YAML payload")

    if not all(isinstance(x, str) for x in payload):
        raise ValueError(
            "YAML payload must contain strings"
        )

    return payload


# ==========================================
# 5. Domain normalization
# ==========================================

DOMAIN_PATTERN = re.compile(
    r"^(?=.{1,253}$)"
    r"(?:[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?\.)+"
    r"[a-z0-9_](?:[a-z0-9_-]{0,61}[a-z0-9_])?$",
    re.IGNORECASE
)


def valid_domain(value):
    return bool(DOMAIN_PATTERN.fullmatch(value))


def valid_keyword(value):

    return bool(
        value
        and len(value) <= 253
        and not any(c.isspace() for c in value)
        and "," not in value
    )


def normalize_domain(raw, source_format):

    line = raw.strip().strip("'\"").strip()

    if not line or line.startswith("#"):
        return None

    if source_format == "classical":

        parts = [x.strip() for x in line.split(",")]

        if len(parts) < 2:
            return None

        kind = parts[0].upper()
        value = parts[1].lower()

        if kind == "DOMAIN":
            if valid_domain(value):
                return "full:" + value
            return None

        if kind == "DOMAIN-SUFFIX":
            if valid_domain(value):
                return "+." + value
            return None

        if kind == "DOMAIN-KEYWORD":
            if valid_keyword(value):
                return "keyword:" + value
            return None

        return None

    # Native domain or plain text rules

    line = line.lower()

    if line.startswith("full:"):

        value = line[5:]

        return line if valid_domain(value) else None

    if line.startswith("keyword:"):

        value = line[8:]

        return line if valid_keyword(value) else None

    if line.startswith("+."):

        value = line[2:]

        return line if valid_domain(value) else None

    if line.startswith("*."):

        value = line[2:]

        return line if valid_domain(value) else None

    if line.startswith("."):

        value = line[1:]

        if valid_domain(value):
            return "+." + value

        return None

    if valid_domain(line):
        return line

    return None


# ==========================================
# 6. IP normalization
# ==========================================

def normalize_ip(raw, source_format):

    line = raw.strip().strip("'\"").strip()

    if not line or line.startswith("#"):
        return None

    if source_format == "classical":

        parts = [x.strip() for x in line.split(",")]

        if len(parts) < 2:
            return None

        kind = parts[0].upper()

        if kind not in ("IP-CIDR", "IP-CIDR6"):
            return None

        line = parts[1]

    elif "," in line:
        return None

    try:

        network = ipaddress.ip_network(
            line,
            strict=False
        )

        return str(network)

    except ValueError:
        return None


# ==========================================
# 7. Generate README
# ==========================================

def generate_readme(rule, count):

    name = rule["name"]
    behavior = rule["behavior"]
    source_format = rule.get("format", "classical")

    raw_url = (
        f"https://raw.githubusercontent.com/"
        f"{REPO}/{BRANCH}/rule/Clash/"
        f"{name}/{name}.mrs"
    )

    cdn_url = (
        f"https://cdn.jsdelivr.net/gh/"
        f"{REPO}@{BRANCH}/rule/Clash/"
        f"{name}/{name}.mrs"
    )

    notice = ""

    if source_format == "classical":

        notice = (
            "\n> 注意：此 MRS 從 Classical 規則中提取"
            "相容的域名或 IP 規則，並非原始 YAML "
            "的完整等價轉換。\n"
        )

    # Use GitHub native code-block copy buttons.
    # No custom JavaScript is required.

    return f"""# {name} MRS 規則

由 GitHub Actions 自動生成，適用於 Mihomo 核心。

## MRS 下載地址

### GitHub Raw

點擊下方程式碼區塊右上角的複製圖示，即可複製完整地址。

```text
{raw_url}
```

**[直接下載 MRS]({raw_url})**

### jsDelivr CDN

點擊下方程式碼區塊右上角的複製圖示，即可複製完整地址。

```text
{cdn_url}
```

**[開啟 CDN 地址]({cdn_url})**

## 規則資訊

| 項目 | 內容 |
|---|---|
| 規則名稱 | {name} |
| 文件格式 | MRS |
| Behavior | {behavior} |
| 規則數量 | {count} |
| 更新頻率 | 每日 |

{notice}
## Mihomo 使用方法

以下配置可使用右上角的複製按鈕，一鍵複製整段。

```yaml
rule-providers:
  {name}:
    type: http
    behavior: {behavior}
    format: mrs
    url: "{raw_url}"
    path: ./ruleset/{name}.mrs
    interval: 86400
```

## 上游來源

<{rule["url"]}>

---

此 README 由 GitHub Actions 自動生成。
"""


# ==========================================
# 8. Build individual MRS
# ==========================================

def build_rule(rule, stage):

    name = rule["name"]
    behavior = rule["behavior"]
    source_format = rule.get("format", "classical")

    print(
        f"\n=== Building {name} ({behavior}) ===",
        flush=True
    )

    content = download(rule["url"])

    payload = parse_source(
        content,
        source_format
    )

    converted = set()
    skipped = 0

    for raw in payload:

        if behavior == "domain":

            value = normalize_domain(
                raw,
                source_format
            )

        else:

            value = normalize_ip(
                raw,
                source_format
            )

        if value:
            converted.add(value)
        else:
            skipped += 1

    minimum = rule.get("min_rules", 1)

    if len(converted) < minimum:

        raise RuntimeError(
            f"{name}: only {len(converted)} valid rules; "
            f"minimum is {minimum}"
        )

    source = TEMP / f"{name}.txt"
    target = OUTPUT / f"{name}.mrs"

    source.write_text(
        "\n".join(sorted(converted)) + "\n",
        encoding="utf-8"
    )

    subprocess.run(
        [
            "mihomo",
            "convert-ruleset",
            behavior,
            "text",
            str(source),
            str(target)
        ],
        check=True
    )

    if not target.is_file() or target.stat().st_size == 0:

        raise RuntimeError(
            f"{name}: missing or empty MRS"
        )

    folder = stage / name

    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    shutil.copyfile(
        target,
        folder / f"{name}.mrs"
    )

    (folder / "README.md").write_text(
        generate_readme(
            rule,
            len(converted)
        ),
        encoding="utf-8"
    )

    print(
        f"SUCCESS: {name} | "
        f"valid={len(converted)} | "
        f"skipped={skipped} | "
        f"size={target.stat().st_size}",
        flush=True
    )


# ==========================================
# 9. Generate SHA256SUMS
# ==========================================

def generate_checksums(stage):

    lines = []

    files = sorted(
        OUTPUT.glob("*.mrs")
    )

    if not files:
        raise RuntimeError("No MRS files generated")

    for path in files:

        digest = hashlib.sha256(
            path.read_bytes()
        ).hexdigest()

        lines.append(
            f"{digest}  {path.name}"
        )

    content = "\n".join(lines) + "\n"

    (OUTPUT / "SHA256SUMS").write_text(
        content,
        encoding="utf-8"
    )

    (stage / "SHA256SUMS").write_text(
        content,
        encoding="utf-8"
    )

    subprocess.run(
        [
            "sha256sum",
            "-c",
            "SHA256SUMS"
        ],
        cwd=OUTPUT,
        check=True
    )


# ==========================================
# 10. Publish completed build
# ==========================================

def publish(stage, rules):

    PUBLISH.mkdir(
        parents=True,
        exist_ok=True
    )

    manifest_path = PUBLISH / MANIFEST

    previous = []

    if manifest_path.exists():

        manifest = json.loads(
            manifest_path.read_text(
                encoding="utf-8"
            )
        )

        previous = manifest.get(
            "managed_rules",
            []
        )

        if not isinstance(previous, list):
            raise RuntimeError(
                "Invalid previous manifest"
            )

        for name in previous:

            if not isinstance(name, str) or not re.fullmatch(
                r"[A-Za-z0-9_-]+",
                name
            ):

                raise RuntimeError(
                    "Unsafe entry in previous manifest"
                )

    current = [
        rule["name"]
        for rule in rules
    ]

    # Remove only previously managed folders.

    for name in previous:

        if name not in current:

            old_folder = PUBLISH / name

            if old_folder.is_dir():

                shutil.rmtree(old_folder)

                print(
                    f"Removed old rule: {name}"
                )

    # Copy all successfully generated files.

    for name in current:

        source_folder = stage / name
        target_folder = PUBLISH / name

        target_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        for filename in (
            f"{name}.mrs",
            "README.md"
        ):

            shutil.copyfile(
                source_folder / filename,
                target_folder / filename
            )

    shutil.copyfile(
        stage / "SHA256SUMS",
        PUBLISH / "SHA256SUMS"
    )

    manifest = {
        "managed_rules": sorted(current)
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )


# ==========================================
# 11. Main
# ==========================================

def main():

    rules = load_config()

    # Clean temporary directories only.

    for folder in (OUTPUT, TEMP):

        if folder.exists():
            shutil.rmtree(folder)

        folder.mkdir(parents=True)

    stage = TEMP / "publish"

    stage.mkdir(
        parents=True
    )

    # Build all rules first.

    for rule in rules:

        build_rule(
            rule,
            stage
        )

    # Verify SHA256 before publishing.

    generate_checksums(stage)

    # Update repository files only after
    # every rule has been built successfully.

    publish(
        stage,
        rules
    )

    print(
        "\nAll MRS rules built and published successfully.",
        flush=True
    )


if __name__ == "__main__":
    main()
