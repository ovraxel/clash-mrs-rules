# Twitch-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitch.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/twitch
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Twitch/Twitch.list

Behavior: `ipcidr`; unique rules: 12.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```

## Mihomo

```yaml
Twitch-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitch-IP/Twitch-IP.mrs
```
