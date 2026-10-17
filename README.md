# 雙格式構建替換包
以舊帳號 wiedergeburtme/clash-mrs-rules 為 fallback；GitHub Actions 執行時自動讀取 GITHUB_REPOSITORY。
將本 ZIP 內檔案按相同路徑覆蓋原倉庫（不要刪除 sources/ 或 rule/ 舊資料）。
本包 config/upstream.json 使用此前 78 服務版本；如果你的私有倉庫已有更新的來源，保留自己的 config/upstream.json 即可。
兩個工作流會同時提交 MRS 和 LIST，手動執行 Actions 測試。
本地 TXT: rule/Shadowrocket/Clash/<Name>/<Name>.list
多來源: rule/Shadowrocket/Upstream/<Provider>/<Name>/<Name>.list
示例: RULE-SET,https://raw.githubusercontent.com/USERNAME/clash-mrs-rules/main/rule/Shadowrocket/Clash/GlobalAI/GlobalAI.list,PROXY
Shadowrocket 的 RULE-SET 內部不附帶策略，策略在引用端指定。
來源中的不支援項目仍依原 upstream 腳本規則跳過；上游網址沒有在本包內逐一聯網驗證。

License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0-only). See the "LICENSE" (LICENSE) file for details.