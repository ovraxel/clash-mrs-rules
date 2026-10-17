# OpenAI

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/openai.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/openai
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list

Behavior: `domain`; unique rules: 50.

Unsupported entries skipped: 2.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/OpenAI/OpenAI.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/OpenAI/OpenAI.mrs
```

## Mihomo

```yaml
OpenAI:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/OpenAI/OpenAI.mrs
```
