# Google-IP

Sources (4):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google.list
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/google.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/google
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.list

Behavior: `ipcidr`; unique rules: 8559.

Unsupported entries skipped: 8.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Google-IP/Google-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Google-IP/Google-IP.mrs
```

## Mihomo

```yaml
Google-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Google-IP/Google-IP.mrs
```
