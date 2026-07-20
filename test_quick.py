"""
Quick Test Script - verify all modules can be imported

各モジュールが正しくインポートできることを確認するテストスクリプト
"""

def test_imports():
    """全てのモジュールのインポートテスト"""
    print("📦 モジュールインポートテスト開始...\n")
    
    try:
        print("✓ work_scheduler.data.models をインポート中...")
        from work_scheduler.data import Task, Deliverable, Theme, DashboardData
        print("  └─ Task, Deliverable, Theme, DashboardData")
        
        print("✓ work_scheduler.data をインポート中...")
        from work_scheduler.data import ExcelReader, WBSParser
        print("  └─ ExcelReader, WBSParser")
        
        print("✓ work_scheduler.business をインポート中...")
        from work_scheduler.business import ProgressCalculator
        print("  └─ ProgressCalculator")
        
        print("✓ work_scheduler.presentation をインポート中...")
        from work_scheduler.presentation import HTMLGenerator
        print("  └─ HTMLGenerator")
        
        print("\n✅ 全てのモジュールが正常にインポートできました！")
        return True
        
    except ImportError as e:
        print(f"\n❌ インポートエラー: {e}")
        print("\n対処方法:")
        print("1. 依存パッケージをインストール: pip install -r requirements.txt")
        print("2. 仮想環境が有効化されているか確認")
        return False
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        return False


def test_data_structures():
    """データ構造の基本テスト"""
    print("\n📊 データ構造テスト開始...\n")
    
    try:
        from datetime import datetime, timedelta
        from work_scheduler.data import Task, Deliverable, Theme
        
        # タスク作成テスト
        print("✓ Task オブジェクト生成テスト...")
        task1 = Task(
            id='task1',
            name='テストタスク1',
            start_date=datetime(2026, 1, 1),
            end_date=datetime(2026, 1, 31),
            status='完了'
        )
        print(f"  └─ Task: {task1.name}, 進捗: {task1.progress}%")
        
        task2 = Task(
            id='task2',
            name='テストタスク2',
            start_date=datetime(2026, 2, 1),
            end_date=datetime(2026, 2, 28),
            status='着手中'
        )
        print(f"  └─ Task: {task2.name}, 進捗: {task2.progress}%")
        
        # 成果物作成テスト
        print("✓ Deliverable オブジェクト生成テスト...")
        deliverable = Deliverable(
            id='del1',
            name='テスト成果物',
            start_date=datetime(2026, 1, 1),
            end_date=datetime(2026, 2, 28),
            tasks=[task1, task2]
        )
        print(f"  └─ Deliverable: {deliverable.name}")
        print(f"    └─ 実績進捗: {deliverable.overall_progress:.1f}%")
        print(f"    └─ 計画進捗: {deliverable.planned_progress:.1f}%")
        
        # テーマ作成テスト
        print("✓ Theme オブジェクト生成テスト...")
        theme = Theme(
            id='theme1',
            name='テストテーマ',
            start_date=datetime(2026, 1, 1),
            end_date=datetime(2026, 2, 28),
            deliverables=[deliverable]
        )
        print(f"  └─ Theme: {theme.name}")
        print(f"    └─ 実績進捗: {theme.overall_progress:.1f}%")
        print(f"    └─ 計画進捗: {theme.planned_progress:.1f}%")
        
        print("\n✅ データ構造テスト完了！")
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("WorkScheduler クイックテスト")
    print("=" * 60 + "\n")
    
    success = True
    
    # インポートテスト
    if not test_imports():
        success = False
    
    # データ構造テスト（インポート成功時のみ）
    if success:
        if not test_data_structures():
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("✅ 全テストが成功しました！")
        print("\n次のステップ:")
        print("1. サンプルExcelファイルを生成:")
        print("   python create_sample.py")
        print("\n2. ダッシュボードを生成:")
        print("   python -m work_scheduler.main sample.xlsx")
        print("\n3. ブラウザで表示:")
        print("   open/start sample_dashboard.html")
    else:
        print("❌ テストに失敗しました")
        print("詳細は上記のエラーメッセージを確認してください")
    print("=" * 60)
