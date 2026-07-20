"""
Excel Reader Module

Excelファイルからデータを読み込むモジュール
"""

import openpyxl
from typing import List, Dict, Optional


class ExcelReader:
    """Excelファイル読み込みクラス
    
    Excelファイルを読み込み、行データのリストを返します。
    """
    
    def __init__(self, filepath: str):
        """初期化
        
        Args:
            filepath: Excelファイルのパス
        """
        self.filepath = filepath
        self.workbook = None
        self.worksheet = None
    
    def read(self) -> List[Dict]:
        """Excelファイルを読み込み、行データのリストを返す
        
        Returns:
            List[Dict]: 行データの辞書リスト
        
        Raises:
            FileNotFoundError: ファイルが見つからない場合
            ValueError: ファイルが無効な場合
        """
        try:
            self.workbook = openpyxl.load_workbook(self.filepath)
        except FileNotFoundError:
            raise FileNotFoundError(f"ファイルが見つかりません: {self.filepath}")
        except Exception as e:
            raise ValueError(f"Excelファイルの読み込みに失敗しました: {e}")
        
        self.worksheet = self.workbook.active
        
        rows = []
        headers = None
        
        # 最初の行をヘッダーとして取得
        for idx, row in enumerate(self.worksheet.iter_rows(values_only=True)):
            if idx == 0:
                headers = row
                continue
            
            if headers is None:
                raise ValueError("ヘッダー行が見つかりません")
            
            # 行データを辞書に変換
            row_dict = {}
            for i, header in enumerate(headers):
                if i < len(row):
                    row_dict[header] = row[i]
                else:
                    row_dict[header] = None
            
            # 空行をスキップ
            if any(v is not None for v in row_dict.values()):
                rows.append(row_dict)
        
        self.workbook.close()
        return rows
    
    def validate(self, rows: List[Dict]) -> bool:
        """バリデーション
        
        Args:
            rows: 行データの辞書リスト
        
        Returns:
            bool: バリデーション成功時True
        
        Raises:
            ValueError: 必須フィールドが見つからない場合
        """
        if not rows:
            raise ValueError("データが見つかりません")
        
        required_fields = ['業務テーマ', '成果物', 'タスク', '開始時期', '終了時期', 'ステータス']
        
        # ヘッダー行をチェック
        sample_row = rows[0]
        missing_fields = [f for f in required_fields if f not in sample_row]
        
        if missing_fields:
            raise ValueError(f"必須フィールドが見つかりません: {missing_fields}")
        
        return True
