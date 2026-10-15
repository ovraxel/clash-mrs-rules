# ChinaMedia-IP

Sources (2):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/category-media-cn.list
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ChinaMedia/ChinaMedia.list

Behavior: `ipcidr`; unique rules: 84.

Unsupported entries skipped: 6.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/ChinaMedia-IP/ChinaMedia-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/ChinaMedia-IP/ChinaMedia-IP.mrs
```

## Mihomo

```yaml
ChinaMedia-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/ChinaMedia-IP/ChinaMedia-IP.mrs
```
