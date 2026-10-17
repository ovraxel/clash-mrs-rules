# Speedtest

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/speedtest.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/speedtest
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Speedtest/Speedtest.list

Behavior: `domain`; unique rules: 18.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Speedtest/Speedtest.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Speedtest/Speedtest.mrs
```

## Mihomo

```yaml
Speedtest:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Speedtest/Speedtest.mrs
```
