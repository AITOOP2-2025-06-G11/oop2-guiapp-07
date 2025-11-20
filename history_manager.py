import json
import os
from datetime import datetime

class HistoryManager:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = []
        self.load_history()

    def load_history(self):
        """履歴ファイルを読み込む"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.history = []
        else:
            self.history = []

    def add_history(self, text, file_path):
        """新しい履歴を追加して保存する"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "text": text,
            "file_path": file_path
        }
        # 新しいものを先頭に
        self.history.insert(0, entry)
        self.save_history()
        return entry

    def save_history(self):
        """履歴をファイルに保存する"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error saving history: {e}")

    def get_history(self):
        """履歴リストを取得する"""
        return self.history
