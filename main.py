from recordTenSeconds import recordTenSeconds
from transcribeAudio import transcribeAudio
from saveTranscription import saveTranscription

recordTenSeconds()
saveTranscription(transcribeAudio())