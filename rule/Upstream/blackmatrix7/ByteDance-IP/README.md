# ByteDance-IP

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/ByteDance/ByteDance.list)

Behavior: `ipcidr`; unique rules: 1.

Process rules not representable in MRS were omitted: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/ByteDance-IP/ByteDance-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/ByteDance-IP/ByteDance-IP.mrs
```

## Mihomo

```yaml
rule-providers:
  ByteDance-IP:
    type: http
    behavior: ipcidr
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/ByteDance-IP/ByteDance-IP.mrs"
    path: ./ruleset/ByteDance-IP.mrs
    interval: 86400
```
