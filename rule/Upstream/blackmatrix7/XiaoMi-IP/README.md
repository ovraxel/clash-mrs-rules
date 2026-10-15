# XiaoMi-IP

Sources (1):
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/XiaoMi/XiaoMi.list

Behavior: `ipcidr`; unique rules: 9.

Unsupported entries skipped: 2.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/XiaoMi-IP/XiaoMi-IP.mrs
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
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/XiaoMi-IP/XiaoMi-IP.mrs
```
