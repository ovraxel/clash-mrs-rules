# Telegram MRS

由本倉庫 TXT 規則自動轉換；Behavior：`domain`；去重後規則數：**36**。

## GitHub Raw（可用程式碼區塊右上角複製）

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram/Telegram.mrs
```

[開啟／下載 MRS](https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram/Telegram.mrs)

## jsDelivr CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Clash/Telegram/Telegram.mrs
```

## Mihomo 配置

```yaml
rule-providers:
  Telegram:
    type: http
    behavior: domain
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram/Telegram.mrs"
    path: ./ruleset/Telegram.mrs
    interval: 86400
```

## TXT 來源

[sources/domain/Telegram.txt](https://github.com/wiedergeburtme/clash-mrs-rules/blob/main/sources/domain/Telegram.txt)
