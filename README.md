# WorkScheduler

Excel形式のWBS（Work Breakdown Structure）データを読み込み、進捗状況をJiraダッシュボード風のHTMLダッシュボードで可視化するPythonツール。

## 📋 主な機能

- **Excelからの自動読み込み**: WBS形式のExcelファイルを読み込み
- **進捗可視化**: 計画進捗 vs 実績進捗をグラフで比較
- **リスク管理**: 遅延したタスク・成果物・テーマを自動検出
- **ダッシュボード表示**: Jiraダッシュボード相当のUIで可視化
- **進捗率自動計算**: ステータス（完了/着手中/未着手）から進捗率を期間加重平均で算出

## 🚀 クイックスタート

### 1. 環境構築

```bash
# 仮想環境を作成
python -m venv venv

# 仮想環境を有効化
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate  # Windows

# 依存パッケージをインストール
pip install -r requirements.txt
```

### 2. サンプルファイルの生成

```bash
# サンプルExcelファイルを生成
python create_sample.py

# 出力: sample.xlsx
```

### 3. ダッシュボード生成

```bash
# ダッシュボードHTMLを生成
python -m work_scheduler.main sample.xlsx

# 出力: sample_dashboard.html
```

### 4. ブラウザで表示

```bash
# HTMLファイルをブラウザで開く
open sample_dashboard.html  # Mac
xdg-open sample_dashboard.html  # Linux
start sample_dashboard.html  # Windows
```

## 📊 入力ファイル形式

Excel ファイルは以下の列を持つ必要があります：

| 業務テーマ | 成果物 | タスク | 開始時期 | 終了時期 | ステータス |
|---|---|---|---|---|---|
| System Infrastructure | | | 2026-01-15 | 2026-04-30 | - |
| | Server Setup | | 2026-01-15 | 2026-02-28 | - |
| | | Install OS | 2026-01-15 | 2026-01-31 | 完了 |
| | | Configure Network | 2026-02-01 | 2026-02-28 | 完了 |

### 注記
- **WBS形式**: テーマ名と成果物名は各階層の最初の行にのみ記載
- **ステータス**: 「完了」「着手中」「未着手」のいずれか
- **日付形式**: YYYY-MM-DD形式に対応

## 🎯 進捗率の計算ロジック

### タスク進捗率
- **完了**: 100%
- **着手中**: 50%
- **未着手**: 0%

### テーマ・成果物の進捗率
期間加重平均で計算：
```
進捗率 = (各タスクの進捗率 × 各タスク期間) の合計 / 全タスク期間の合計
```

### ステータス判定
- **On Track**: 実績進捗 ≥ 計画進捗
- **At Risk**: 計画進捗 - 10% ≤ 実績進捗 < 計画進捗
- **Delayed**: 実績進捗 < 計画進捗 - 10% または 期限超過

## 📁 プロジェクト構造

```
work_scheduler/
├── data/
│   ├── models.py              # データモデル定義
│   ├── excel_reader.py        # Excel読み込み
│   ├── wbs_parser.py          # WBSパース処理
│   └── __init__.py
├── business/
│   ├── progress_calculator.py # 進捗率計算
│   └── __init__.py
├── presentation/
│   ├── html_generator.py      # HTML生成
│   └── __init__.py
├── utils/
│   └── __init__.py
├── main.py                    # エントリーポイント
└── __init__.py
```

## 🧪 テスト

```bash
# ユニットテスト実行
pytest tests/ -v

# カバレッジ確認
pytest tests/ --cov=work_scheduler
```

## 📖 ドキュメント

- [基本設計書](./基本設計書.md) - システムアーキテクチャ、データモデル
- [実装仕様書](./実装仕様書.md) - 詳細な実装仕様、APIリファレンス
- [開発計画書](./開発計画書.md) - 開発スケジュール、リスク管理

## 🔧 オプション

### 出力ファイルの指定

```bash
python -m work_scheduler.main input.xlsx custom_output.html
```

### ロギングの有効化

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## ⚙️ システム要件

- Python 3.8以上
- openpyxl 3.0以上
- pandas 1.3以上
- Jinja2 3.0以上

## 📝 使用例

```python
from work_scheduler.data import ExcelReader, WBSParser, DashboardData
from work_scheduler.presentation import HTMLGenerator

# Excelファイルを読み込み
reader = ExcelReader('input.xlsx')
rows = reader.read()

# WBSをパース
parser = WBSParser()
themes = parser.parse(rows)

# ダッシュボードデータを生成
from datetime import datetime
dashboard = DashboardData(themes=themes, generated_at=datetime.now())

# HTMLを生成
html = HTMLGenerator.generate(dashboard)

# ファイルに保存
with open('output.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

## 🐛 トラブルシューティング

### ファイルが見つからないエラー

```
ファイルが見つかりません: input.xlsx
```

→ ファイルパスを確認してください

### 日付フォーマットエラー

```
日付形式が無効です: 2026/1/1
```

→ YYYY-MM-DD形式を使用してください

### メモリ不足エラー

大規模なWBS（1000タスク以上）では、メモリ使用量が増加する可能性があります。

## 📞 サポート

- GitHub Issues: [issues](https://github.com/your-repo/issues)
- Email: support@example.com

## 📄 ライセンス

MIT License

## 🙏 謝辞

このプロジェクトはJira ダッシュボードのUIデザインに大きなインスピレーションを受けています。

---

**バージョン**: 1.0.0  
**最終更新**: 2026年7月21日
