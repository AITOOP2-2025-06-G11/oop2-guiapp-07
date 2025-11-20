# work2
import mlx_whisper
from pydub import AudioSegment
import numpy as np

def transcribeAudio():
	print("transcribeAudio")

	# 音声ファイルを指定して文字起こし
	audio_file_path = "python-audio-output.wav"

	result = mlx_whisper.transcribe(
			audio_file_path, path_or_hf_repo="./whisper-base-mlx"
	)
	print(result)
	# resultは辞書形式なので、'text'キーでテキストを取得
	return result['text']