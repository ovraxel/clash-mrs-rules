# Spotify

Upstream: [blackmatrix7](https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Spotify/Spotify.list)

Behavior: `domain`; unique rules: 27.

Non-domain/IP rules omitted: 1.

## Raw

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Spotify/Spotify.mrs
```

## CDN

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Upstream/blackmatrix7/Spotify/Spotify.mrs
```

## Mihomo

```yaml
Spotify:
    type: http
    behavior: domain
    format: mrs
    interval: 86400
    url: https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Upstream/blackmatrix7/Spotify/Spotify.mrs
```
