# telegram MRS 規則

由 GitHub Actions 自動生成，適用於 Mihomo 核心。

## 規則鏈接

### MAIN 分支（每日更新）

<https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/telegram/telegram.mrs>

### MAIN 分支 CDN（每日更新）

<https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Clash/telegram/telegram.mrs>

## 規則資訊

| 項目 | 說明 |
|---|---|
| 規則名稱 | telegram |
| 文件格式 | MRS |
| Behavior | domain |
| 更新頻率 | 每日 |
## | 最後構建日期 | 2026-10-14 |

## Mihomo 使用方法

```yaml
rule-providers:
  telegram:
    type: http
    behavior: domain
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/telegram/telegram.mrs"
    path: ./ruleset/telegram.mrs
    interval: 86400
```

## 上游來源

<https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Telegram/Telegram.yaml>

---

此 README 由 GitHub Actions 自動生成，請勿手動修改。
