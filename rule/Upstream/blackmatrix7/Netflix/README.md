# Netflix

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Netflix/Netflix.list)

Behavior: `domain`; unique rules: 37.

Non-domain/IP rules omitted: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Netflix/Netflix.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Netflix/Netflix.mrs
```

## Mihomo

```yaml
Netflix:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Netflix/Netflix.mrs
```
