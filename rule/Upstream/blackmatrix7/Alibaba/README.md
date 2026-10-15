# Alibaba

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/alibaba.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/alibaba
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Alibaba/Alibaba.list

Behavior: `domain`; unique rules: 1492.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/Alibaba/Alibaba.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Alibaba/Alibaba.mrs
```

## Mihomo

```yaml
Alibaba:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/Alibaba/Alibaba.mrs
```
