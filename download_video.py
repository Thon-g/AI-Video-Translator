import os
import subprocess

def download_youtube_audio(url, output_dir="downloads"):
    os.makedirs(output_dir, exist_ok=True)
    # đặt tên file theo tiêu đề video
    output_path = os.path.join(output_dir, "%(title)s.mp4")
    cmd = [
        "yt-dlp",
        "-f", "best",
        "--merge-output-format", "mp4",
        "-o", output_path,
        url
    ]
    subprocess.run(cmd, check=True)

    # lấy file mới tải
    files = sorted(
        [os.path.join(output_dir, f) for f in os.listdir(output_dir)],
        key=os.path.getctime,
        reverse=True
    )
    if files:
        return files[0]   # file mới nhất
    return None