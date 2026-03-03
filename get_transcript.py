import gc
import torch
from faster_whisper import WhisperModel


def get_transcript(audio_path):
    # Giải phóng VRAM và RAM trước khi load Whisper
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()

    model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")

    segments, info = model.transcribe(audio_path, beam_size=5)
    segments_list = list(segments)

    # Ghép toàn bộ text từ các đoạn
    full_text = "".join(seg.text for seg in segments_list)

    result = {
        "text": full_text.strip(),
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in segments_list
        ],
        "language": info.language
    }

    if model is not None:
        del model
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

    return result

