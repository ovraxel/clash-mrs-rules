# MailServices MRS

由本倉庫 TXT 規則自動轉換；Behavior：`domain`；去重後規則數：**21**。

## GitHub Raw（可用程式碼區塊右上角複製）

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/MailServices/MailServices.mrs
```

[開啟／下載 MRS](https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/MailServices/MailServices.mrs)

## jsDelivr CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Clash/MailServices/MailServices.mrs
```

## Mihomo 配置

```yaml
MailServices:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/MailServices/MailServices.mrs
```

## TXT 來源

[sources/domain/MailServices.txt](https://github.com/ovraxel/clash-mrs-rules/blob/main/sources/domain/MailServices.txt)
