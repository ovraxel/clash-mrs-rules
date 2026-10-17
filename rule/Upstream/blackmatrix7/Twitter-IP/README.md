# Twitter-IP

Sources (4):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/twitter.list
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geoip/twitter.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/twitter
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Twitter/Twitter.list

Behavior: `ipcidr`; unique rules: 22.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitter-IP/Twitter-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Twitter-IP/Twitter-IP.mrs
```

## Mihomo

```yaml
Twitter-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Twitter-IP/Twitter-IP.mrs
```
