# Stripe

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/stripe.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/stripe
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Stripe/Stripe.list

Behavior: `domain`; unique rules: 9.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Stripe/Stripe.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Stripe/Stripe.mrs
```

## Mihomo

```yaml
Stripe:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Stripe/Stripe.mrs
```
