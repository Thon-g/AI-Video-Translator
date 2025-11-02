import asyncio
import os
import subprocess
from pathlib import Path
import streamlit as st
from adjust_audio import list_adjust_tempo
from concat_file import merge_tts_segments, merge_video_audio
from download_video import download_youtube_audio
from get_transcript import get_transcript
from language_map import language_map
from split_video_audio import split_video_audio
from test import translate_segments
from text_to_speech import text_to_speech, convertMp3ToWav
from vocal_isolation import isolate_vocals
from voice_map import voice_map


def get_output_filename(input_path: str, suffix="_completed", ext=".mp4"):
    p = Path(input_path)
    return str(p.with_name(p.stem + suffix + ext))


# --- Thư mục ---
os.makedirs("uploads", exist_ok=True)
os.makedirs("split_temp", exist_ok=True)
os.makedirs("final", exist_ok=True)

st.title("Quéo căm tu mai áp")

option = st.radio(
    "Chọn nguồn đầu vào:",
    ["📂 Upload file video", "🔗 Nhập URL YouTube"]
)

if "video_file" not in st.session_state:
    st.session_state.video_file = None

# --- Upload / Youtube ---
if option == "📂 Upload file video":
    uploaded_file = st.file_uploader("Chọn 1 file video", type=["mp4", "mov", "m3u8"])
    if uploaded_file:
        save_path = Path("uploads")
        video_path = save_path / uploaded_file.name
        with open(video_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Đã lưu file tại: {video_path}")
        st.session_state.video_file = str(video_path)

elif option == "🔗 Nhập URL YouTube":
    url = st.text_input("Nhập link YouTube:")
    if url and st.button("Tải video từ YouTube"):
        try:
            video_path = download_youtube_audio(url, "uploads")
            st.success(f"Đã tải xong video: {video_path}")
            st.session_state.video_file = video_path
        except subprocess.CalledProcessError as e:
            st.error(f"Lỗi tải video: {e}")

# --- Chọn ngôn ngữ / voice ---
target_lang_code = st.selectbox(
    "Chọn ngôn ngữ cần dịch",
    options=list(language_map.keys()),
    format_func=lambda x: language_map[x]
)

voices_for_lang = voice_map.get(target_lang_code, [])
voice_selected = st.selectbox(
    "Chọn giọng đọc",
    options=voices_for_lang
)


video_no_audio = os.path.join("split_temp", "video_no_audio.mp4")
audio = os.path.join("split_temp", "audio.wav")
audio_concat = os.path.join("final", "audio_concated.wav")

# --- Nút xử lý ---
if st.session_state.video_file:
    if st.button("Bắt đầu xử lý video"):
        final_output = os.path.join("final", Path(st.session_state.video_file).stem + "_completed.mp4")
        with st.spinner("Đang xử lý ! Đợi xíu đi, hơi lâu đó..."):
            status = st.empty()
            # Tách video / audio
            status.write("Đang tách video và audio...")
            video_no_audio, audio_path = split_video_audio(st.session_state.video_file, video_no_audio, audio)

            status.write("Đang tách vocal và audio nền...")
            vocals_path, no_vocals_path = isolate_vocals(audio_path, "split_temp")

            # Lấy transcript
            status.write("Đang lấy transcript...")
            result = get_transcript(vocals_path)
            segments = result["segments"]
            origin_lang_code = result["language"]

            # Dịch
            status.write(f"Đang dịch transcript sang ngôn ngữ {language_map[target_lang_code]}...")
            list_text_origin = [seg["text"] for seg in segments if seg["text"].strip()]
            for i in range(3):
                translated = translate_segments(segments, origin_lang_code, target_lang_code)

                # translated = asyncio.run(translate_segments_async(segments, origin_lang_code, target_lang_code, model="qwen3", batch_size=20))
                # LỌC BỎ segments rỗng
                translated_filtered = [seg for seg in translated if seg['text'].strip()]
                list_text = [seg['text'] for seg in translated_filtered]

                duration_list = [seg["end"] - seg["start"] for seg in segments]
                count_positive = sum(duration > 0 for duration in duration_list)
                if len(list_text) == count_positive:
                    break

            # Text to speech
            status.write("Đang chuyển văn bản thành giọng nói...")
            audio_tts_dir = asyncio.run(text_to_speech(list_text, voice_selected))
            convertMp3ToWav(audio_tts_dir)

            abspath_tts_dir = os.path.abspath(audio_tts_dir)
            list_target_duration = [float(seg['end'] - seg['start']) for seg in translated_filtered]

            # Chỉnh tốc độ
            status.write("Đang điều chỉnh lại tốc độ đọc...")
            list_adjust_tempo(audio_tts_dir, list_target_duration, abspath_tts_dir)

            # Nối audio
            status.write("Đang nối các list audio thành một...")
            merged_vocal_path = merge_tts_segments(translated_filtered, abspath_tts_dir, audio_concat)

            # Ghép video
            status.write("Đang ghép audio và video lại với nhau ...")
            final_video = merge_video_audio(video_no_audio, merged_vocal_path, no_vocals_path, final_output)
            status.empty()

        st.success(f"Hoàn tất! Video đã lưu tại: {final_video}")
        st.video(final_video)

        # # tải video về
        # with open(final_video, "rb") as file:
        #     st.download_button(
        #         label="Tải file",
        #         data=file,
        #         file_name=final_output,
        #         mime="video/mp4"
        #     )
