import re
import subprocess, os, json
from pydub.utils import mediainfo

def get_duration(audio_file):
    """Trả về duration (giây, float) hoặc None nếu không đọc được."""
    if not os.path.exists(audio_file):
        raise FileNotFoundError(f"File không tồn tại: {audio_file}")

    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        audio_file
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        print(f"[WARN] ffprobe lỗi cho file {audio_file}: {proc.stderr}")
        return None

    try:
        info = json.loads(proc.stdout)
    except json.JSONDecodeError:
        print(f"[WARN] Không parse được JSON ffprobe cho file {audio_file}")
        return None

    dur = info.get("format", {}).get("duration")
    if not dur:
        print(f"[WARN] Không xác định được duration cho file {audio_file}")
        return None

    return float(dur)


def _build_atempo_filter(rate: float):
    """
    Nếu rate nằm trong [0.5, 2.0] -> trả về "atempo=rate".
    Nếu ngoài -> tách thành nhiều atempo, ví dụ rate=4.0 -> atempo=2.0,atempo=2.0
    return string filter cho ffmpeg (dùng -af hoặc -filter:a).
    """
    if rate <= 0:
        raise ValueError("rate phải > 0")
    factors = []
    # reduce large rates by factors of 2
    while rate > 2.0:
        factors.append(2.0)
        rate /= 2.0
    # increase small rates by factors of 0.5
    while rate < 0.5:
        factors.append(0.5)
        rate /= 0.5
    # remaining factor
    # clamp small floating error
    if abs(rate - 1.0) > 1e-6:
        factors.append(rate)
    # build filter string
    filter_parts = [f"atempo={f:.6f}" for f in factors]
    # if no factors (rate == 1.0) return empty string
    return ",".join(filter_parts) if filter_parts else ""



def adjust_tempo(input_file, target_duration, output_file=None, overwrite=False):
    """
    Điều chỉnh tempo của input_file để khớp target_duration.
    - Nếu audio TTS nhanh hơn (ngắn hơn target) -> giữ nguyên (không chỉnh).
    - Nếu audio TTS chậm hơn (dài hơn target) -> tua nhanh để khớp.
    """
    if output_file is None and not overwrite:
        raise ValueError("Phải chỉ định output_file hoặc overwrite=True để ghi đè file gốc.")

    duration_tts = get_duration(input_file)
    if target_duration <= 0:
        raise ValueError("target_duration phải > 0")

    # chỉ chỉnh khi TTS dài hơn target
    if duration_tts <= target_duration:
        if overwrite:
            return input_file
        else:
            os.replace(input_file, output_file)   # copy logic đơn giản
            return output_file

    # cần tua nhanh
    rate = duration_tts / float(target_duration)

    # nếu rate ≈ 1.0 thì copy thôi
    if abs(rate - 1.0) < 1e-3:
        if overwrite:
            return input_file
        else:
            os.replace(input_file, output_file)
            return output_file

    filter_expr = _build_atempo_filter(rate)
    if not filter_expr:
        if overwrite:
            return input_file
        else:
            os.replace(input_file, output_file)
            return output_file

    # chuẩn bị output tạm
    if output_file is None:
        tmp_out = input_file + ".tmp.wav"
        final_out = input_file
    else:
        tmp_out = output_file + ".tmp.wav"
        final_out = output_file

    cmd = [
        "ffmpeg", "-y",
        "-i", input_file,
        "-af", filter_expr,
        tmp_out
    ]

    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg atempo lỗi:\ncmd={' '.join(cmd)}\nstderr:\n{proc.stderr}")

    # replace tmp -> final
    os.replace(tmp_out, final_out)
    return final_out


def list_adjust_tempo(audio_tts_dir, list_target_duration, output_dir=None, overwrite=False):
    """
    audio_tts_dir: thư mục chứa các file TTS (ví dụ "0.wav","1.wav",...)
    list_target_duration: danh sách duration mục tiêu (giây), thứ tự tương ứng
    output_dir: nơi lưu file đã adjust (mặc định = audio_tts_dir)
    overwrite: nếu True thì ghi đè file gốc để tên giữ nguyên (0.wav,...)
    Trả về danh sách file đã được adjust (đường dẫn).
    """
    if output_dir is None:
        output_dir = audio_tts_dir
    # liệt kê file .wav và sort theo số ở tên file (nếu có)
    files = [f for f in os.listdir(audio_tts_dir) if f.lower().endswith(".wav")]
    # cố gắng sort theo số ở đầu tên (0.wav,1.wav,...). nếu không parse được, fallback sort lexicographic
    def _key(fname):
        name = os.path.splitext(fname)[0]
        m = re.match(r"^(\d+)$", name)
        if m:
            return int(m.group(1))
        # thử lấy số anywhere
        m2 = re.search(r"(\d+)", name)
        if m2:
            return int(m2.group(1))
        return name
    files = sorted(files, key=_key)

    if len(files) != len(list_target_duration):
        raise ValueError(f"Số file ({len(files)}) không khớp số target durations ({len(list_target_duration)}).")

    out_files = []
    for i, fname in enumerate(files):
        input_path = os.path.join(audio_tts_dir, fname)
        target = float(list_target_duration[i])
        if overwrite:
            output_path = input_path  # will be replaced
        else:
            # giữ tên giống nhưng lưu vào output_dir (có thể cùng thư mục hoặc khác)
            output_path = os.path.join(output_dir, fname)
            # nếu output_dir == audio_tts_dir and filename collides we write to tmp then replace
        # print(f"[INFO] Adjusting {input_path} -> target {target:.3f}s")
        out = adjust_tempo(input_path, target, output_path, overwrite=overwrite)
        new_dur = get_duration(out)
        # print(f"[DONE] {fname}: {new_dur:.3f}s (target {target:.3f}s)")
        out_files.append(out)
    return out_files

