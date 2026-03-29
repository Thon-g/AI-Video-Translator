import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import gc
import torch
from faster_whisper import WhisperModel


def get_transcript(audio_path):
    # Giải phóng VRAM và RAM trước khi load Whisper
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
    gc.collect()
    print("[get_transcript] VRAM cleaned, loading model...")
    model = WhisperModel("medium", device="cuda" if torch.cuda.is_available() else "cpu", compute_type="float16")

    print("[get_transcript] Model loaded. Starting transcription (with VAD enabled)...")
    segments, info = model.transcribe(audio_path, beam_size=5, vad_filter=True, vad_parameters=dict(min_silence_duration_ms=500))
    
    print("[get_transcript] Transcription finished, converting generator to list...")
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

