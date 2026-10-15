# OpenAI-IP

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/openai
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list

Behavior: `ipcidr`; unique rules: 2.

Unsupported entries skipped: 2.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/OpenAI-IP/OpenAI-IP.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/OpenAI-IP/OpenAI-IP.mrs
```

## Mihomo

```yaml
OpenAI-IP:
    type: http
    behavior: ipcidr
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/refs/heads/main/rule/Upstream/blackmatrix7/OpenAI-IP/OpenAI-IP.mrs
```
