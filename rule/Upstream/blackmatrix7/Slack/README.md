# Slack

Sources (3):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/slack.list
- https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/slack
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Slack/Slack.list

Behavior: `domain`; unique rules: 11.

Unsupported entries skipped: 0.

## Raw

```text
https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Slack/Slack.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/ovraxel/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Slack/Slack.mrs
```

## Mihomo

```yaml
Slack:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/ovraxel/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Slack/Slack.mrs
```
