# Claude Code サブエージェント

このリポジトリ（Neural Overflow フロントエンド）用の役割別エージェントです。メインのClaudeが必要に応じて委譲します。

| 名前 | モデル | 役割 |
|---|---|---|
| frontend-implementer | sonnet | HTML/CSS/JSの実装・修正（唯一編集可能） |
| ui-mobile-checker | haiku | モバイル表示・タップ性の点検（読み取り専用） |
| seo-copy-reviewer | sonnet | title/OGP/sitemap/文章のレビュー（提案のみ） |
| security-auditor | sonnet | 秘密情報・XSS・Actions設定の監査（読み取り専用） |

## 並列利用の頼み方（例）
- 「ui-mobile-checkerとseo-copy-reviewerに並列で index.html と about.html を調べさせて、最後に統合して重要度順の修正リストにして」
- 「security-auditorで監査 → 指摘のうち高だけをfrontend-implementerに直させて」
