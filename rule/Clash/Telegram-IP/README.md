# Telegram-IP MRS

由本倉庫 TXT 規則自動轉換；Behavior：`ipcidr`；去重後規則數：**27**。

## GitHub Raw（可用程式碼區塊右上角複製）

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram-IP/Telegram-IP.mrs
```

[開啟／下載 MRS](https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram-IP/Telegram-IP.mrs)

## jsDelivr CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Clash/Telegram-IP/Telegram-IP.mrs
```

## Mihomo 配置

```yaml
rule-providers:
  Telegram-IP:
    type: http
    behavior: ipcidr
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/Telegram-IP/Telegram-IP.mrs"
    path: ./ruleset/Telegram-IP.mrs
    interval: 86400
```

## TXT 來源

[sources/ip/Telegram-IP.txt](https://github.com/wiedergeburtme/clash-mrs-rules/blob/main/sources/ip/Telegram-IP.txt)
