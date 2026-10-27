# Session-IP MRS

由本倉庫 TXT 規則自動轉換；Behavior：`ipcidr`；去重後規則數：**7**。

## GitHub Raw（可用程式碼區塊右上角複製）

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/Session-IP/Session-IP.mrs
```

[開啟／下載 MRS](https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/Session-IP/Session-IP.mrs)

## jsDelivr CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Clash/Session-IP/Session-IP.mrs
```

## Mihomo 配置

```yaml
Session-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Clash/Session-IP/Session-IP.mrs
```

## TXT 來源

[sources/ip/Session-IP.txt](https://github.com/ovraxel/clash-mrs-rules/blob/main/sources/ip/Session-IP.txt)
