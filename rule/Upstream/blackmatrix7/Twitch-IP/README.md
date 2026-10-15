# Twitch-IP

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Twitch/Twitch.list)

Behavior: `ipcidr`; unique rules: 12.

Non-domain/IP rules omitted: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```

## Mihomo

```yaml
Twitch-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```
