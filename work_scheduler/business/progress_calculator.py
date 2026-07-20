"""
Progress Calculator Module

進捗率を計算するモジュール
"""

from datetime import datetime
from typing import List

from ..data.models import Task, Deliverable, Theme


class ProgressCalculator:
    """進捗率計算クラス
    
    タスク、成果物、テーマの進捗率を計算します。
    """
    
    @staticmethod
    def calculate_planned_progress(start_date: datetime, end_date: datetime) -> float:
        """計画進捗を計算（スケジュール進捗）
        
        計画進捗 = (Today - Start Date) / (End Date - Start Date) * 100
        
        Args:
            start_date: 開始日
            end_date: 終了日
        
        Returns:
            float: 計画進捗率（0-100）
        """
        today = datetime.now()
        total_days = (end_date - start_date).days
        elapsed_days = (today - start_date).days
        
        if total_days <= 0:
            return 0.0
        
        progress = (elapsed_days / total_days) * 100
        return min(100.0, max(0.0, progress))
    
    @staticmethod
    def calculate_actual_progress(tasks: List[Task]) -> float:
        """実績進捗を計算（期間加重平均）
        
        実績進捗 = (各タスクの進捗率 × 各タスク期間) の合計 / 全タスク期間の合計
        
        タスク進捗率：
            - '完了': 100%
            - '着手中': 50%
            - '未着手': 0%
        
        Args:
            tasks: タスクのリスト
        
        Returns:
            float: 実績進捗率（0-100）
        """
        if not tasks:
            return 0.0
        
        total_duration = sum(t.duration_days for t in tasks)
        if total_duration == 0:
            return 0.0
        
        weighted_progress = sum(t.progress * t.duration_days for t in tasks)
        return (weighted_progress / total_duration)
    
    @staticmethod
    def calculate_deliverable_progress(deliverable: Deliverable) -> float:
        """成果物の進捗率を計算
        
        Args:
            deliverable: 成果物オブジェクト
        
        Returns:
            float: 進捗率（0-100）
        """
        return ProgressCalculator.calculate_actual_progress(deliverable.tasks)
    
    @staticmethod
    def calculate_theme_progress(theme: Theme) -> float:
        """テーマの進捗率を計算
        
        Args:
            theme: テーマオブジェクト
        
        Returns:
            float: 進捗率（0-100）
        """
        all_tasks = [task for d in theme.deliverables for task in d.tasks]
        return ProgressCalculator.calculate_actual_progress(all_tasks)
