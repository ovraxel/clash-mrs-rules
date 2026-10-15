# YouTube-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/youtube.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/youtube
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/YouTube/YouTube.list

Behavior: `ipcidr`; unique rules: 3.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/YouTube-IP/YouTube-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/YouTube-IP/YouTube-IP.mrs
```

## Mihomo

```yaml
YouTube-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/YouTube-IP/YouTube-IP.mrs
```
