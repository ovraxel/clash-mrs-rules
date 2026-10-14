
# ==========================================
# 7. Generate README
# ==========================================

def generate_readme(rule, folder, count):

    name = rule["name"]
    behavior = rule["behavior"]

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

    lines = [
        f"# {name} MRS 規則",
        "",
        "由 GitHub Actions 自動生成，適用於 Mihomo 核心。",
        "",
        "## 規則鏈接",
        "",
        f"### {BRANCH.upper()} 分支（每日更新）",
        "",
        f"<{raw_url}>",
        "",
        f"### {BRANCH.upper()} 分支 CDN（每日更新）",
        "",
        f"<{cdn_url}>",
        "",
        "## 規則資訊",
        "",
        "| 項目 | 說明 |",
        "|---|---|",
        f"| 規則名稱 | {name} |",
        "| 文件格式 | MRS |",
        f"| Behavior | {behavior} |",
        f"| 規則數量 | {count} |",
        "| 更新頻率 | 每日 |",
        "",
        "## Mihomo 使用方法",
        "",
        "    rule-providers:",
        f"      {name}:",
        "        type: http",
        f"        behavior: {behavior}",
        "        format: mrs",
        f'        url: "{raw_url}"',
        f"        path: ./ruleset/{name}.mrs",
        "        interval: 86400",
        "",
        "## 上游來源",
        "",
        f"<{rule['url']}>",
        "",
        "---",
        "",
        "此 README 由 GitHub Actions 自動生成。",
        ""
    ]

    readme = "\n".join(lines)

    path = folder / "README.md"

    path.write_text(
        readme,
        encoding="utf-8"
    )

    print(f"README generated: {path}")
