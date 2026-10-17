# Telegram-IP

Sources (4):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/telegram.list
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/telegram.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/telegram
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Telegram/Telegram.list

Behavior: `ipcidr`; unique rules: 18.

Unsupported entries skipped: 11.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Telegram-IP/Telegram-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Telegram-IP/Telegram-IP.mrs
```

## Mihomo

```yaml
Telegram-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Telegram-IP/Telegram-IP.mrs
```
