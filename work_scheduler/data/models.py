"""
Work Scheduler Data Models

このモジュールは、WorkSchedulerの主要なデータモデルを定義します。
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Task:
    """タスククラス
    
    Attributes:
        id: タスクID（UUID）
        name: タスク名
        deliverable_id: 所属する成果物のID
        start_date: 開始日
        end_date: 終了日
        status: ステータス（'完了', '着手中', '未着手'）
    """
    id: str
    name: str
    deliverable_id: str
    start_date: datetime
    end_date: datetime
    status: str  # '完了', '着手中', '未着手'
    
    @property
    def progress(self) -> float:
        """ステータスに基づいた進捗率を返す (0-100)
        
        Returns:
            float: 進捗率
                - '完了': 100.0
                - '着手中': 50.0
                - '未着手': 0.0
        """
        if self.status == '完了':
            return 100.0
        elif self.status == '着手中':
            return 50.0
        else:  # '未着手'
            return 0.0
    
    @property
    def duration_days(self) -> int:
        """タスク期間（日数）
        
        Returns:
            int: 期間日数
        """
        return (self.end_date - self.start_date).days + 1
    
    @property
    def days_delayed(self) -> int:
        """遅延日数を計算
        
        Returns:
            int: 遅延日数（遅延していない場合は0）
        """
        if self.status != '完了' and datetime.now() > self.end_date:
            return (datetime.now() - self.end_date).days
        return 0
    
    @property
    def is_delayed(self) -> bool:
        """遅延判定
        
        Returns:
            bool: 遅延している場合True
        """
        return self.days_delayed > 0


@dataclass
class Deliverable:
    """成果物クラス
    
    Attributes:
        id: 成果物ID（UUID）
        name: 成果物名
        theme_id: 所属するテーマのID
        start_date: 開始日
        end_date: 終了日
        tasks: 含まれるタスクのリスト
    """
    id: str
    name: str
    theme_id: str
    start_date: datetime
    end_date: datetime
    tasks: List[Task] = field(default_factory=list)
    
    @property
    def status(self) -> str:
        """含まれるタスクのステータスから判定
        
        Returns:
            str: ステータス（'完了', '着手中', '未着手'）
        """
        if not self.tasks:
            return '未着手'
        
        completed = sum(1 for t in self.tasks if t.status == '完了')
        in_progress = sum(1 for t in self.tasks if t.status == '着手中')
        
        if completed == len(self.tasks):
            return '完了'
        elif in_progress > 0 or completed > 0:
            return '着手中'
        else:
            return '未着手'
    
    @property
    def overall_progress(self) -> float:
        """期間加重平均で進捗率を計算
        
        Returns:
            float: 進捗率（0-100）
                = (各タスクの進捗率 × 各タスク期間) の合計 / 全タスク期間の合計
        """
        if not self.tasks:
            return 0.0
        
        total_duration = sum(t.duration_days for t in self.tasks)
        if total_duration == 0:
            return 0.0
        
        weighted_progress = sum(t.progress * t.duration_days for t in self.tasks)
        return (weighted_progress / total_duration)
    
    @property
    def planned_progress(self) -> float:
        """計画進捗（スケジュール進捗）
        
        Returns:
            float: 進捗率（0-100）
                = (Today - Start Date) / (End Date - Start Date) * 100
        """
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (datetime.now() - self.start_date).days
        
        if total_days <= 0:
            return 0.0
        
        return min(100.0, max(0.0, (elapsed_days / total_days) * 100))


@dataclass
class Theme:
    """業務テーマクラス
    
    Attributes:
        id: テーマID（UUID）
        name: テーマ名
        start_date: 開始日
        end_date: 終了日
        deliverables: 含まれる成果物のリスト
    """
    id: str
    name: str
    start_date: datetime
    end_date: datetime
    deliverables: List[Deliverable] = field(default_factory=list)
    
    @property
    def status(self) -> str:
        """ステータス判定
        
        Returns:
            str: ステータス
                - 'On Track': 実績進捗 >= 計画進捗
                - 'At Risk': 計画進捗 - 10% <= 実績進捗 < 計画進捗
                - 'Delayed': 実績進捗 < 計画進捗 - 10% または 期限超過
        """
        if self.overall_progress >= self.planned_progress:
            return 'On Track'
        elif self.overall_progress >= self.planned_progress - 10:
            return 'At Risk'
        else:
            return 'Delayed'
    
    @property
    def overall_progress(self) -> float:
        """期間加重平均で進捗率を計算
        
        Returns:
            float: 進捗率（0-100）
        """
        all_tasks = [task for d in self.deliverables for task in d.tasks]
        
        if not all_tasks:
            return 0.0
        
        total_duration = sum(t.duration_days for t in all_tasks)
        if total_duration == 0:
            return 0.0
        
        weighted_progress = sum(t.progress * t.duration_days for t in all_tasks)
        return (weighted_progress / total_duration)
    
    @property
    def planned_progress(self) -> float:
        """計画進捗（スケジュール進捗）
        
        Returns:
            float: 進捗率（0-100）
        """
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (datetime.now() - self.start_date).days
        
        if total_days <= 0:
            return 0.0
        
        return min(100.0, max(0.0, (elapsed_days / total_days) * 100))


@dataclass
class DashboardData:
    """ダッシュボード用データクラス
    
    Attributes:
        themes: テーマのリスト
        generated_at: 生成時刻
    """
    themes: List[Theme]
    generated_at: datetime
    
    @property
    def overall_progress(self) -> float:
        """全体進捗率（実績）
        
        Returns:
            float: 進捗率（0-100）
        """
        all_tasks = [task for t in self.themes for d in t.deliverables for task in d.tasks]
        
        if not all_tasks:
            return 0.0
        
        total_duration = sum(t.duration_days for t in all_tasks)
        if total_duration == 0:
            return 0.0
        
        weighted_progress = sum(t.progress * t.duration_days for t in all_tasks)
        return (weighted_progress / total_duration)
    
    @property
    def overall_planned_progress(self) -> float:
        """全体計画進捗（スケジュール進捗）
        
        Returns:
            float: 進捗率（0-100）
        """
        if not self.themes:
            return 0.0
        
        return sum(t.planned_progress for t in self.themes) / len(self.themes)
    
    @property
    def delayed_items(self) -> List[tuple]:
        """遅延アイテム一覧
        
        Returns:
            List[tuple]: (アイテム種別, アイテムオブジェクト) のリスト
        """
        delayed = []
        
        for theme in self.themes:
            if theme.overall_progress < theme.planned_progress:
                delayed.append(('theme', theme))
            
            for deliv in theme.deliverables:
                if deliv.overall_progress < deliv.planned_progress:
                    delayed.append(('deliverable', deliv))
                
                for task in deliv.tasks:
                    if task.is_delayed:
                        delayed.append(('task', task))
        
        return delayed
    
    @property
    def in_progress_items(self) -> List[tuple]:
        """進行中アイテム一覧
        
        Returns:
            List[tuple]: (アイテム種別, アイテムオブジェクト) のリスト
        """
        in_progress = []
        
        for theme in self.themes:
            if theme.status == 'In Progress' or theme.status == 'At Risk':
                in_progress.append(('theme', theme))
            
            for deliv in theme.deliverables:
                if deliv.status == '着手中':
                    in_progress.append(('deliverable', deliv))
                
                for task in deliv.tasks:
                    if task.status == '着手中':
                        in_progress.append(('task', task))
        
        return in_progress
    
    @property
    def total_tasks_count(self) -> int:
        """タスク総数"""
        return sum(len(d.tasks) for t in self.themes for d in t.deliverables)
    
    @property
    def completed_tasks_count(self) -> int:
        """完了タスク数"""
        return sum(
            sum(1 for task in d.tasks if task.status == '完了')
            for t in self.themes for d in t.deliverables
        )
    
    @property
    def in_progress_tasks_count(self) -> int:
        """進行中タスク数"""
        return sum(
            sum(1 for task in d.tasks if task.status == '着手中')
            for t in self.themes for d in t.deliverables
        )
    
    @property
    def not_started_tasks_count(self) -> int:
        """未着手タスク数"""
        return sum(
            sum(1 for task in d.tasks if task.status == '未着手')
            for t in self.themes for d in t.deliverables
        )
    
    @property
    def delayed_tasks_count(self) -> int:
        """遅延タスク数"""
        return sum(
            1 for _, item in self.delayed_items
            if isinstance(item, Task)
        )
