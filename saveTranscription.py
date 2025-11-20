# work3

import os
import datetime

def saveTranscription(text, output_dir="transcriptions"):
	os.makedirs(output_dir, exist_ok=True)
	timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
	filename = f"transcription_{timestamp}.txt"
	save_path = os.path.join(output_dir, filename)
	with open(save_path, "w", encoding="utf-8") as f:
			f.write(text)
	print(f" 文字起こし結果を保存しました: {save_path}")
	return save_path
