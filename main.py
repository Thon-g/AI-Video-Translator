from get_transcript import *
from vocal_isolation import isolate_vocals
from translate_transcript import *
from text_to_speech import *
from adjust_audio import *
from concat_file import *
from split_video_audio import *

target_lang_code = ""
voice = ""
video_input = ""

video_no_audio, audio_path = split_video_audio(video_input, "split_temp/video_no_audio.mp4", "split_temp/audio.wav")

vocals_path, no_vocals_path = isolate_vocals(audio_path, "split_temp")

# lấy trascript
print("lấy trascript")
result = get_transcript(vocals_path)

# dịch transcirpt và trả về dict translated
print("dịch transcirpt và trả về dict translated")
segments = result["segments"]
orin_lang_code = result["language"]
translated = translate_segments(segments, orin_lang_code, target_lang_code)

# text to speech bản dịch
print("text to speech bản dịch")
list_text = [tran['text'] for tran in translated]
audio_tts_dir = asyncio.run(text_to_speech(list_text, voice))
print("convert audio mp3 sang wav")
convertMp3ToWav(audio_tts_dir)

abspath_tts_dir = os.path.abspath(os.path.join(audio_tts_dir))
list_target_duration = [float(seg['end']-seg['start']) for seg in translated]

# chỉnh lại tốc độ đọc của audio tts
print("chỉnh lại tốc độ đọc của audio tts")
list_adjust_tempo(audio_tts_dir, list_target_duration, abspath_tts_dir)

# nối audio lại với timeline
print("nối audio lại với timeline")
merged_vocal_path = merge_tts_segments(translated, abspath_tts_dir, "final/final_audio.wav")

# ghép video với audio
print("ghép video với audio")
final_video = merge_video_audio(video_no_audio, merged_vocal_path, no_vocals_path, "final/final_video.mp4")

print("xong")