# requirements-engineering

要求の出所・要件品質・設計判断・受入検証をつなぐ、日本語の共通ガイドとAIエージェント用スキルです。要求・要件・基本設計の作成やレビュー、リポジトリの新規作成・更新差分の監査に使えます。

入口は[requirements-engineeringスキル](skills/requirements-engineering/SKILL.md)です。文書の一覧と検証手順は[SITEMAP](SITEMAP.md)を参照してください。

## AIエージェントに読ませる

[生のSKILL.md](https://raw.githubusercontent.com/hogehonya/requirements-engineering/main/skills/requirements-engineering/SKILL.md)をエージェントへ渡してください。必要に応じてリンク先の[参照資料](skills/requirements-engineering/references/sources.md)も読ませます。スキルはこのリポジトリ固有のパスや他のスキルに依存せず、ディレクトリ単位で使えます。

## インストール

リポジトリを対象プロジェクトとは別の作業場所へcloneし、対象エージェントが対応するスキル配置先へ `skills/requirements-engineering` 全体をコピーします。以下はプロジェクト内の `.agents/skills` を読むエージェント向けの例です。既存の配置先がある場合は上書きせず、別の保存先を選んでください。

```sh
git clone https://github.com/hogehonya/requirements-engineering.git
cd requirements-engineering
mkdir -p /path/to/project/.agents/skills
if [ -e /path/to/project/.agents/skills/requirements-engineering ] || [ -L /path/to/project/.agents/skills/requirements-engineering ]; then
  echo 'requirements-engineering already exists; choose another destination' >&2
  false
else
  cp -R skills/requirements-engineering /path/to/project/.agents/skills/requirements-engineering
fi
```

エージェントごとに配置先とスキル呼び出し方法を確認してください。コピーしたスキル内にガイド、参照資料、ライセンスが含まれます。通常のMarkdownガイドとして読むこともできます。

## 適用範囲と根拠

このガイドは要求の出所と目的、要件の品質、設計への対応、変更と検証の追跡という4つの判断軸をまとめた独自の運用整理です。規格本文や書籍本文の転載ではなく、規格への準拠・認証を主張するものでもありません。参照した公開資料と確認範囲は[文献と適用の根拠](skills/requirements-engineering/references/sources.md)に記載しています。

レビューや監査の依頼は読み取り専用として扱い、編集は明示された依頼範囲に限ります。このスキルはそれ自体でIssue作成や外部送信を許可しません。パッケージと同梱のスキルは[MIT License](LICENSE)で配布します。参照資料の本文や第三者の著作物は同梱しておらず、このライセンスの対象外です。

## 検証

Python 3.9以上の標準ライブラリだけで実行できます。

```sh
python3 scripts/check.py
```

必須ファイル、frontmatter、Markdownの相対リンク、代表的な環境固有参照を確認します。これはパッケージ構造の検査であり、外部URLの到達性、要求判断の品質、スキルの自動選択を測るものではありません。pushとpull requestでも同じ検査を実行します。
