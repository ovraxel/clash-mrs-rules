# Amazon-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/amazon.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/amazon
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Amazon/Amazon.list

Behavior: `ipcidr`; unique rules: 15.

Unsupported entries skipped: 4.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Amazon-IP/Amazon-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Amazon-IP/Amazon-IP.mrs
```

## Mihomo

```yaml
Amazon-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Amazon-IP/Amazon-IP.mrs
```
