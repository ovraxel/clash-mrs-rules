# NetEaseMusic-IP

Sources (1):
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/NetEaseMusic/NetEaseMusic.list

Behavior: `ipcidr`; unique rules: 18.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/NetEaseMusic-IP/NetEaseMusic-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/NetEaseMusic-IP/NetEaseMusic-IP.mrs
```

## Mihomo

```yaml
NetEaseMusic-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/NetEaseMusic-IP/NetEaseMusic-IP.mrs
```
