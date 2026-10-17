# XiaoMi-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/xiaomi.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/xiaomi
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/XiaoMi/XiaoMi.list

Behavior: `ipcidr`; unique rules: 9.

Unsupported entries skipped: 2.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/XiaoMi-IP/XiaoMi-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/XiaoMi-IP/XiaoMi-IP.mrs
```

## Mihomo

```yaml
XiaoMi-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/XiaoMi-IP/XiaoMi-IP.mrs
```
