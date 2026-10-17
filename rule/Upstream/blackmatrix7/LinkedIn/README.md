# LinkedIn

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/linkedin.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/linkedin
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/LinkedIn/LinkedIn.list

Behavior: `domain`; unique rules: 15.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/LinkedIn/LinkedIn.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/LinkedIn/LinkedIn.mrs
```

## Mihomo

```yaml
LinkedIn:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/LinkedIn/LinkedIn.mrs
```
