# China-IP

Sources (2):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/cn.list
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/China/China.list

Behavior: `ipcidr`; unique rules: 21.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/China-IP/China-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/China-IP/China-IP.mrs
```

## Mihomo

```yaml
China-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/China-IP/China-IP.mrs
```
