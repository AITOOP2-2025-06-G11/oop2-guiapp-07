import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox, QListWidget, QSplitter
from PySide6.QtCore import QThread, Signal, Qt
from recordTenSeconds import recordTenSeconds
from transcribeAudio import transcribeAudio
from saveTranscription import saveTranscription
from history_manager import HistoryManager

class Worker(QThread):
    finished = Signal(object)
    error = Signal(str)

    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))

class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.history_manager = HistoryManager()
        self.initUI()
        self.load_history_to_ui()

    def initUI(self):
        self.setWindowTitle('Audio Transcription App with History')
        self.setGeometry(100, 100, 800, 500)

        # メインレイアウト（左右分割）
        main_layout = QHBoxLayout()

        # --- 左側：操作パネル ---
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.status_label = QLabel('待機中')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        left_layout.addWidget(self.status_label)

        # 録音ボタン
        self.record_btn = QPushButton('録音開始 (10秒)')
        self.record_btn.clicked.connect(self.start_recording)
        left_layout.addWidget(self.record_btn)

        # 文字起こしボタン
        self.transcribe_btn = QPushButton('文字起こし開始')
        self.transcribe_btn.clicked.connect(self.start_transcription)
        self.transcribe_btn.setEnabled(False)
        left_layout.addWidget(self.transcribe_btn)

        # 結果表示エリア
        left_layout.addWidget(QLabel("実行結果:"))
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        left_layout.addWidget(self.result_area)

        # --- 右側：履歴リスト ---
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        right_layout.addWidget(QLabel("履歴 (クリックで詳細表示):"))
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_clicked)
        right_layout.addWidget(self.history_list)

        # スプリッターで左右を分割（サイズ調整可能に）
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([500, 300]) # 初期サイズ比率

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

    def load_history_to_ui(self):
        """履歴データをリストに表示する"""
        self.history_list.clear()
        history = self.history_manager.get_history()
        for entry in history:
            # リストには日時を表示
            self.history_list.addItem(entry['timestamp'])

    def on_history_clicked(self, item):
        """履歴がクリックされたときの処理"""
        # クリックされた項目のインデックスを取得
        index = self.history_list.row(item)
        history = self.history_manager.get_history()
        
        if 0 <= index < len(history):
            entry = history[index]
            self.result_area.setText(f"--- 履歴詳細 ---\n日時: {entry['timestamp']}\n保存先: {entry['file_path']}\n\n内容:\n{entry['text']}")

    def start_recording(self):
        self.status_label.setText('録音中... (10秒間)')
        self.record_btn.setEnabled(False)
        self.transcribe_btn.setEnabled(False)
        self.result_area.append("--- 録音を開始します ---")
        
        # 録音処理を別スレッドで実行
        self.record_worker = Worker(recordTenSeconds)
        self.record_worker.finished.connect(self.on_recording_finished)
        self.record_worker.error.connect(self.on_error)
        self.record_worker.start()

    def on_recording_finished(self, result):
        self.status_label.setText('録音完了')
        self.record_btn.setEnabled(True)
        self.transcribe_btn.setEnabled(True)
        self.result_area.append("録音が完了しました。")

    def start_transcription(self):
        self.status_label.setText('文字起こし中...')
        self.record_btn.setEnabled(False)
        self.transcribe_btn.setEnabled(False)
        self.result_area.append("--- 文字起こしを開始します ---")

        # 文字起こし処理を別スレッドで実行
        self.transcribe_worker = Worker(transcribeAudio)
        self.transcribe_worker.finished.connect(self.on_transcription_finished)
        self.transcribe_worker.error.connect(self.on_error)
        self.transcribe_worker.start()

    def on_transcription_finished(self, text):
        self.status_label.setText('文字起こし完了')
        self.record_btn.setEnabled(True)
        self.transcribe_btn.setEnabled(True)
        self.result_area.append(f"結果:\n{text}")
        
        try:
            save_path = saveTranscription(text)
            self.result_area.append(f"\n保存先: {save_path}")
            
            # 履歴に追加
            self.history_manager.add_history(text, save_path)
            self.load_history_to_ui() # リスト更新
            
        except Exception as e:
            self.result_area.append(f"\n保存エラー: {e}")

    def on_error(self, error_msg):
        self.status_label.setText('エラー発生')
        self.record_btn.setEnabled(True)
        self.transcribe_btn.setEnabled(True)
        QMessageBox.critical(self, "エラー", f"処理中にエラーが発生しました:\n{error_msg}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioApp()
    window.show()
    sys.exit(app.exec())