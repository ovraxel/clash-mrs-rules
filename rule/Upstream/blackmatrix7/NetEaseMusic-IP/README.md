# NetEaseMusic-IP

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/NetEaseMusic/NetEaseMusic.list)

Behavior: `ipcidr`; unique rules: 18.

Non-domain/IP rules omitted: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/NetEaseMusic-IP/NetEaseMusic-IP.mrs
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
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/NetEaseMusic-IP/NetEaseMusic-IP.mrs
```
