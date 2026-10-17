# GlobalMedia-IP

Sources (1):
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/GlobalMedia/GlobalMedia.list

Behavior: `ipcidr`; unique rules: 924.

Unsupported entries skipped: 3.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/GlobalMedia-IP/GlobalMedia-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/GlobalMedia-IP/GlobalMedia-IP.mrs
```

## Mihomo

```yaml
GlobalMedia-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/GlobalMedia-IP/GlobalMedia-IP.mrs
```
