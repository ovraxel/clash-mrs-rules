# telegram-ip MRS 規則

由 GitHub Actions 自動生成，適用於 Mihomo 核心。

## MRS 下載地址

### GitHub Raw

點擊下方程式碼區塊右上角的複製圖示，即可複製完整地址。

```text
https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/telegram-ip/telegram-ip.mrs
```

**[直接下載 MRS](https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/telegram-ip/telegram-ip.mrs)**

### jsDelivr CDN

點擊下方程式碼區塊右上角的複製圖示，即可複製完整地址。

```text
https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Clash/telegram-ip/telegram-ip.mrs
```

**[開啟 CDN 地址](https://cdn.jsdelivr.net/gh/wiedergeburtme/clash-mrs-rules@main/rule/Clash/telegram-ip/telegram-ip.mrs)**

## 規則資訊

| 項目 | 內容 |
|---|---|
| 規則名稱 | telegram-ip |
| 文件格式 | MRS |
| Behavior | ipcidr |
| 規則數量 | 10 |
| 更新頻率 | 每日 |


> 注意：此 MRS 從 Classical 規則中提取相容的域名或 IP 規則，並非原始 YAML 的完整等價轉換。

## Mihomo 使用方法

以下配置可使用右上角的複製按鈕，一鍵複製整段。

```yaml
rule-providers:
  telegram-ip:
    type: http
    behavior: ipcidr
    format: mrs
    url: "https://raw.githubusercontent.com/wiedergeburtme/clash-mrs-rules/main/rule/Clash/telegram-ip/telegram-ip.mrs"
    path: ./ruleset/telegram-ip.mrs
    interval: 86400
```

## 上游來源

<https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Telegram/Telegram.yaml>

---

此 README 由 GitHub Actions 自動生成。
