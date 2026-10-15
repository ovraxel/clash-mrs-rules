# Facebook

Sources (4):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/facebook.list
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/facebook.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/facebook
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Facebook/Facebook.list

Behavior: `domain`; unique rules: 553.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/Facebook/Facebook.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Facebook/Facebook.mrs
```

## Mihomo

```yaml
Facebook:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/Facebook/Facebook.mrs
```
