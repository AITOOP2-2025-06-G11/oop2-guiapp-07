import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QMessageBox
from PySide6.QtCore import Qt

class AudioApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Audio Transcription App (UI Only)')
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
        self.status_label.setText('録音ボタンが押されました')
        self.result_area.append("--- 録音処理（未実装） ---")
        # UIの動作確認のため、ボタンの状態を変更
        self.transcribe_btn.setEnabled(True)

    def start_transcription(self):
        self.status_label.setText('文字起こしボタンが押されました')
        self.result_area.append("--- 文字起こし処理（未実装） ---")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AudioApp()
    window.show()
    sys.exit(app.exec())