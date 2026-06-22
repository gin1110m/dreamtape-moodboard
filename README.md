# dreamtape — Art Direction Guide

dreamtape（Satoru × Ginpei）のアートディレクション・ガイド兼ムードボード。白地16:9のHTMLスライドデッキ。

**Live:** https://gin1110m.github.io/dreamtape-moodboard/ （`?lang=ja` / `?lang=en`）

## 編集（Claude Code 推奨）
このリポジトリには `CLAUDE.md` が入っているので、Claude Code が規約（ブランドDNA・レイアウト方式・日本語の作り方・壊してはいけない点）を自動で把握する。まずはそれに任せるのが速い。

```bash
git clone https://github.com/gin1110m/dreamtape-moodboard.git
cd dreamtape-moodboard
# index.html をブラウザで開けばプレビューできる（ローカルサーバ不要）
```

## 構成
- `index.html` — デッキ全体（CSS・JS・多言語辞書まで1ファイルに同梱）。
- `assets/` — 画像。
- `scripts/gen_i18n_zwsp.py` — 日本語テキスト生成（BudouXで改行最適化）。

## 公開
`git push`（main）→ GitHub Pages が自動デプロイ（約1分）。共有URLは `?v=<short-sha>` を付ける。

## 日本語を直すとき
`index.html` の `const I18N = {...}` は手で触らない。`scripts/gen_i18n_zwsp.py` の `DICT` を直して:

```bash
pip install budoux
python3 scripts/gen_i18n_zwsp.py
```

詳細・ルールは `CLAUDE.md` を参照。
