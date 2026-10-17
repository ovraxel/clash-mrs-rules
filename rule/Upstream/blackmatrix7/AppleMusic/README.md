# AppleMusic

Sources (2):
- https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta/geo/geosite/apple-music.list
- https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/AppleMusic/AppleMusic.list

Behavior: `domain`; unique rules: 24.

Unsupported entries skipped: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/AppleMusic/AppleMusic.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/AppleMusic/AppleMusic.mrs
```

## Mihomo

```yaml
AppleMusic:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/AppleMusic/AppleMusic.mrs
```
