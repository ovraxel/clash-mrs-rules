# Hulu

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/hulu.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/hulu
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Hulu/Hulu.list

Behavior: `domain`; unique rules: 59.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Hulu/Hulu.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Hulu/Hulu.mrs
```

## Mihomo

```yaml
Hulu:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Hulu/Hulu.mrs
```
