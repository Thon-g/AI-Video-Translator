import shutil
import subprocess
import os

def isolate_vocals(input_audio_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    model_name = "htdemucs"
    cmd = [
        "demucs",
        "-n", model_name,
        "--two-stems", "vocals",
        "-o", output_dir,
        input_audio_path
    ]
    subprocess.run(cmd, check=True)
    # Tìm file kết quả trong thư mục con
    input_filename = os.path.splitext(os.path.basename(input_audio_path))[0]
    demucs_dir = os.path.join(output_dir, model_name, input_filename)

    vocals_src = os.path.join(demucs_dir, "vocals.wav")
    no_vocals_src = os.path.join(demucs_dir, "no_vocals.wav")

    # Copy (hoặc move) về output_dir gốc
    vocals_dst = os.path.join(output_dir, "vocals.wav")
    no_vocals_dst = os.path.join(output_dir, "no_vocals.wav")

    shutil.move(vocals_src, vocals_dst)
    shutil.move(no_vocals_src, no_vocals_dst)

    # Xóa folder phụ
    shutil.rmtree(os.path.join(output_dir, model_name))

    return vocals_dst, no_vocals_dst


# audio_path = "split_temp\\audio1.wav"
# vocals_path, no_vocals_path = isolate_vocals(audio_path, "split_temp")
# print(vocals_path)
# print(no_vocals_path)