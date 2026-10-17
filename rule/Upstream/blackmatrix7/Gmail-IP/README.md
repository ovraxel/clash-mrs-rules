# Gmail-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/google.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/google
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.list

Behavior: `ipcidr`; unique rules: 5.

Unsupported entries skipped: 8.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Gmail-IP/Gmail-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Gmail-IP/Gmail-IP.mrs
```

## Mihomo

```yaml
Gmail-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Gmail-IP/Gmail-IP.mrs
```
