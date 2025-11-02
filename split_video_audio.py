import subprocess


def split_video_audio(input_video, output_video="video_no_audio.mp4", output_audio="audio.wav"):
    # Tách audio
    command_audio = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", input_video,  # input
        "-q:a", "0",  # chất lượng audio cao nhất
        "-map", "a",  # chỉ lấy audio
        output_audio
    ]

    # Tách video (mute)
    command_video = [
        "ffmpeg",
        "-y",
        "-i", input_video,
        "-an",  # remove audio
        "-c:v", "copy",  # giữ nguyên video (không encode lại)
        output_video
    ]

    subprocess.run(command_audio, check=True)
    subprocess.run(command_video, check=True)

    return output_video, output_audio
