"""
WBS Parser Module

WBS形式のデータをパースするモジュール
"""

from typing import List, Dict
from datetime import datetime
import uuid

from .models import Theme, Deliverable, Task


class WBSParser:
    """WBSデータパーサークラス
    
    WBS形式のデータをパースして、Theme→Deliverable→Taskの階層構造に変換します。
    """
    
    def __init__(self):
        """初期化"""
        self.themes = []
        self.current_theme = None
        self.current_deliverable = None
    
    def parse(self, rows: List[Dict]) -> List[Theme]:
        """WBS形式のデータをパース
        
        Args:
            rows: 行データの辞書リスト
        
        Returns:
            List[Theme]: パース済みのテーマリスト
        """
        self.themes = []
        self.current_theme = None
        self.current_deliverable = None
        
        for row in rows:
            theme_name = (row.get('業務テーマ') or '').strip()
            deliv_name = (row.get('成果物') or '').strip()
            task_name = (row.get('タスク') or '').strip()
            
            start_date = self._parse_date(row.get('開始時期'))
            end_date = self._parse_date(row.get('終了時期'))
            status = (row.get('ステータス') or '未着手').strip()
            
            # Theme処理（業務テーマが記載されている行）
            if theme_name:
                self.current_theme = Theme(
                    id=str(uuid.uuid4()),
                    name=theme_name,
                    start_date=start_date,
                    end_date=end_date,
                    deliverables=[]
                )
                self.themes.append(self.current_theme)
                self.current_deliverable = None
            
            # Deliverable処理（成果物が記載されている行）
            if deliv_name and self.current_theme:
                self.current_deliverable = Deliverable(
                    id=str(uuid.uuid4()),
                    name=deliv_name,
                    theme_id=self.current_theme.id,
                    start_date=start_date,
                    end_date=end_date,
                    tasks=[]
                )
                self.current_theme.deliverables.append(self.current_deliverable)
            
            # Task処理（タスクが記載されている行）
            if task_name and self.current_deliverable:
                task = Task(
                    id=str(uuid.uuid4()),
                    name=task_name,
                    deliverable_id=self.current_deliverable.id,
                    start_date=start_date,
                    end_date=end_date,
                    status=status
                )
                self.current_deliverable.tasks.append(task)
        
        return self.themes
    
    @staticmethod
    def _parse_date(date_value) -> datetime:
        """日付値をdatetimeに変換
        
        Args:
            date_value: 日付値（datetime、文字列、またはNone）
        
        Returns:
            datetime: 変換後の日付
        
        Raises:
            ValueError: 日付形式が無効な場合
        """
        if isinstance(date_value, datetime):
            return date_value
        
        if date_value is None:
            return datetime.now()
        
        date_str = str(date_value).strip()
        
        # 複数の日付フォーマットに対応
        formats = [
            '%Y-%m-%d',
            '%Y/%m/%d',
            '%Y年%m月%d日',
            '%m/%d/%Y',
            '%m-%d-%Y',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"日付形式が無効です: {date_value}")
