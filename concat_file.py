from pydub import AudioSegment
import os
import subprocess

def merge_tts_segments(translated, audio_dir, output_path="merged.wav"):
    # Tính tổng thời gian của file output
    total_duration = int(max(seg['end'] for seg in translated) * 1000)
    output = AudioSegment.silent(duration=total_duration)

    for i, seg in enumerate(translated):
        start_ms = int(seg['start'] * 1000)
        file_path = os.path.join(audio_dir, f"{i}.wav")
        if not os.path.exists(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue

        audio = AudioSegment.from_wav(file_path)

        # Overlay vào timeline
        output = output.overlay(audio, position=start_ms)

    output.export(output_path, format="wav")
    return output_path



def merge_video_audio(video_path, vocal_path, audio_path, output_path="final_video.mp4"):
    # -c:v copy  => giữ nguyên video, không re-encode
    # -c:a aac   => encode audio thành AAC (chuẩn cho MP4)
    # -shortest  => cắt video hoặc audio theo cái ngắn hơn để không bị lệch
    command = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", vocal_path,
        "-i", audio_path,
        "-filter_complex", "[1:a][2:a]amix=inputs=2:duration=shortest[aout]",
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(command, check=True)
    return output_path

