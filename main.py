import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
from PySide6.QtCore import QThread, Signal, Qt
from recordTenSeconds import recordTenSeconds
from transcribeAudio import transcribeAudio
from saveTranscription import saveTranscription

# Note: Requirements mentioned "Photo acquisition" and "Image synthesis".
# In this Audio project context:
# - "Photo acquisition" -> "Audio Recording"
# - "Image synthesis" -> "Transcription"

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
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Transcription App')
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.status_label = QLabel('待機中')
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.status_label)

        # 録音ボタン
        self.record_btn = QPushButton('録音開始 (10秒)')
        self.record_btn.clicked.connect(self.start_recording)
        layout.addWidget(self.record_btn)

        # 文字起こしボタン
        self.transcribe_btn = QPushButton('文字起こし開始')
        self.transcribe_btn.clicked.connect(self.start_transcription)
        self.transcribe_btn.setEnabled(False)
        layout.addWidget(self.transcribe_btn)

        # 結果表示エリア
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        layout.addWidget(self.result_area)

        self.setLayout(layout)

    def start_recording(self):
        self.status_label.setText('録音中... (10秒間)')
        self.record_btn.setEnabled(False)
        self.transcribe_btn.setEnabled(False)
        self.result_area.append("--- 録音を開始します ---")
        
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