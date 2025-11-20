import ffmpeg
import time


# work1
def recordTenSeconds():
	"""
	10秒間録音する関数
	
	マイクからの音声を10秒間録音し、WAVファイルとして保存する。
	
	Output:
		./python-audio-output.wav: 録音されたオーディオファイル
	"""
	# 録音時間（秒）
	duration = 10
	# 出力ファイル名
	output_file = 'python-audio-output.wav'

	try:
			print(f"{duration}秒間、マイクからの録音を開始します...")
			# FFmpegコマンドを実行
			# -f <デバイス入力形式>: OSに応じたデバイス入力形式を指定
			#   - Windows: 'dshow' または 'gdigrab'
			#   - macOS: 'avfoundation'
			#   - Linux: 'alsa'
			# -i <入力デバイス名>: デバイス名を指定
			(
					ffmpeg
					.input(':1', format='avfoundation', t=duration) # macOSの例
					.output(output_file, acodec='pcm_s16le', ar='44100', ac=1)
					.run(overwrite_output=True)
			)
			print(f"録音が完了しました。{output_file}に保存されました。")

	except ffmpeg.Error as e:
			print(f"エラーが発生しました: {e.stderr.decode()}")
	except Exception as e:
			print(f"予期せぬエラー: {e}")
