# BiliBili-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/bilibili.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/bilibili
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/BiliBili/BiliBili.list

Behavior: `ipcidr`; unique rules: 8.

Unsupported entries skipped: 6.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/BiliBili-IP/BiliBili-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/BiliBili-IP/BiliBili-IP.mrs
```

## Mihomo

```yaml
BiliBili-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/BiliBili-IP/BiliBili-IP.mrs
```
