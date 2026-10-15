# TencentVideo-IP

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/TencentVideo/TencentVideo.list)

Behavior: `ipcidr`; unique rules: 32.

Non-domain/IP rules omitted: 0.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/TencentVideo-IP/TencentVideo-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/TencentVideo-IP/TencentVideo-IP.mrs
```

## Mihomo

```yaml
TencentVideo-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/TencentVideo-IP/TencentVideo-IP.mrs
```
