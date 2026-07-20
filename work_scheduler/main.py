"""
Work Scheduler Main Entry Point

WorkSchedulerツールのメイン処理
"""

import sys
from pathlib import Path
from datetime import datetime

from work_scheduler.data import ExcelReader, WBSParser, DashboardData
from work_scheduler.presentation import HTMLGenerator


def main(input_file: str, output_file: str = None):
    """メイン処理
    
    Args:
        input_file: 入力Excelファイルのパス
        output_file: 出力HTMLファイルのパス（デフォルト: input_file_dashboard.html）
    
    Returns:
        bool: 成功時True
    """
    try:
        # 入力ファイルの確認
        input_path = Path(input_file)
        if not input_path.exists():
            print(f"エラー: ファイルが見つかりません: {input_file}")
            return False
        
        # 出力ファイルの決定
        if output_file is None:
            output_file = str(input_path.stem) + "_dashboard.html"
        
        print(f"📂 入力ファイルを読み込み中: {input_file}")
        reader = ExcelReader(str(input_path))
        rows = reader.read()
        
        print(f"✓ {len(rows)}行のデータを読み込みました")
        
        # バリデーション
        print(f"🔍 データをバリデーション中...")
        reader.validate(rows)
        print(f"✓ バリデーション完了")
        
        # WBS パース処理
        print(f"📊 WBS構造をパース中...")
        parser = WBSParser()
        themes = parser.parse(rows)
        print(f"✓ {len(themes)}個のテーマをパースしました")
        
        # ダッシュボードデータの生成
        print(f"📈 ダッシュボードデータを生成中...")
        dashboard_data = DashboardData(
            themes=themes,
            generated_at=datetime.now()
        )
        
        # 統計情報の出力
        print(f"  - タスク総数: {dashboard_data.total_tasks_count}")
        print(f"  - 完了済み: {dashboard_data.completed_tasks_count}")
        print(f"  - 進行中: {dashboard_data.in_progress_tasks_count}")
        print(f"  - 未着手: {dashboard_data.not_started_tasks_count}")
        print(f"  - 遅延中: {dashboard_data.delayed_tasks_count}")
        print(f"  - 全体進捗: {dashboard_data.overall_progress:.1f}%")
        
        # HTML生成
        print(f"🎨 HTMLダッシュボードを生成中...")
        html = HTMLGenerator.generate(dashboard_data)
        
        # HTMLファイルの書き込み
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✓ ダッシュボードを生成しました: {output_file}")
        print(f"📊 完了！")
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("使用方法: python -m work_scheduler.main <excel_file> [output_file]")
        print("")
        print("例:")
        print("  python -m work_scheduler.main input.xlsx")
        print("  python -m work_scheduler.main input.xlsx output.html")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = main(input_file, output_file)
    sys.exit(0 if success else 1)
