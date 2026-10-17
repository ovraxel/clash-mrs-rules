# Reddit

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/reddit.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/reddit
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Reddit/Reddit.list

Behavior: `domain`; unique rules: 15.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Reddit/Reddit.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Reddit/Reddit.mrs
```

## Mihomo

```yaml
Reddit:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Reddit/Reddit.mrs
```
