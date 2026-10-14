
import json
import hashlib
import ipaddress
import pathlib
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUTPUT = ROOT / "output"
TEMP = ROOT / ".build"

OUTPUT.mkdir(exist_ok=True)
TEMP.mkdir(exist_ok=True)

with open(ROOT / "config/sources.json", encoding="utf-8") as f:
    config = json.load(f)


def download(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Clash-MRS-Builder/1.0"}
    )

    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read(20 * 1024 * 1024 + 1)

    if len(data) > 20 * 1024 * 1024:
        raise ValueError("Source exceeds 20 MB")

    return data.decode("utf-8-sig")


def normalize(line, behavior):
    line = line.strip()

    if not line or line.startswith("#"):
        return None

    # Support simple Clash payload lists
    if line == "payload:":
        return None

    if line.startswith("- "):
        line = line[2:].strip()

    line = line.strip("'\"").strip()

    if not line or line.startswith("#"):
        return None

    if behavior == "domain":
        upper = line.upper()

        mapping = {
            "DOMAIN-SUFFIX,": "",
            "DOMAIN,": "full:",
            "DOMAIN-KEYWORD,": "keyword:",
        }

        for prefix, replacement in mapping.items():
            if upper.startswith(prefix):
                value = line[len(prefix):].split(",")[0].strip()
                return replacement + value.lower() if value else None

        # Plain domain / Mihomo text syntax
        if "," not in line and " " not in line:
            return line.lower()

        return None

    if behavior == "ipcidr":
        upper = line.upper()

        if upper.startswith(("IP-CIDR,", "IP-CIDR6,")):
            line = line.split(",")[1].strip()

        try:
            network = ipaddress.ip_network(line, strict=False)
            return str(network)
        except ValueError:
            return None

    raise ValueError(f"Unsupported behavior: {behavior}")


def build(rule):
    name = rule["name"]
    behavior = rule["behavior"]

    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"Invalid rule name: {name}")

    if behavior not in ("domain", "ipcidr"):
        raise ValueError(f"Unsupported behavior: {behavior}")

    print(f"\nBuilding {name} ({behavior})", flush=True)

    content = download(rule["url"])
    lines = set()

    for raw in content.splitlines():
        value = normalize(raw, behavior)
        if value:
            lines.add(value)

    if not lines:
        raise RuntimeError(f"No valid rules found: {name}")

    source = TEMP / f"{name}.txt"
    target = OUTPUT / f"{name}.mrs"

    source.write_text(
        "\n".join(sorted(lines)) + "\n",
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

    if not target.exists() or target.stat().st_size == 0:
        raise RuntimeError(f"Invalid output: {target}")

    print(
        f"SUCCESS: {name}, {len(lines)} rules, "
        f"{target.stat().st_size} bytes",
        flush=True
    )


names = [rule["name"] for rule in config["rules"]]

if len(names) != len(set(names)):
    raise ValueError("Duplicate rule names")

if not names:
    raise ValueError("No rules configured")

for rule in config["rules"]:
    build(rule)


# Generate checksums
checksum_file = OUTPUT / "SHA256SUMS"

with checksum_file.open("w", encoding="utf-8") as f:
    for path in sorted(OUTPUT.glob("*.mrs")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        f.write(f"{digest}  {path.name}\n")

print("\nAll MRS rules built successfully.")


# Publish MRS files into GitHub directory structure

import shutil

PUBLISH_DIR = ROOT / "rule" / "Clash"

for rule in config["rules"]:
    name = rule["name"]

    source = OUTPUT / f"{name}.mrs"

    if not source.is_file():
        raise RuntimeError(f"Missing MRS: {source}")

    folder = PUBLISH_DIR / name
    folder.mkdir(parents=True, exist_ok=True)

    target = folder / f"{name}.mrs"

    shutil.copy2(source, target)

    print(f"Published: {target}")

shutil.copy2(
    OUTPUT / "SHA256SUMS",
    PUBLISH_DIR / "SHA256SUMS"
)

