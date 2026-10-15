# ByteDance

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ByteDance/ByteDance.list)

Behavior: `domain`; unique rules: 370.

Process rules not representable in MRS were omitted: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/ByteDance/ByteDance.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/ByteDance/ByteDance.mrs
```

## Mihomo

```yaml
rule-providers:
  ByteDance:
    type: http
    behavior: domain
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/ByteDance/ByteDance.mrs"
    path: ./ruleset/ByteDance.mrs
    interval: 86400
```
