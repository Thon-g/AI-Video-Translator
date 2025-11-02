from faster_whisper import WhisperModel

def get_transcript(audio_path):
    model = WhisperModel("small", device="cuda", compute_type="float16")
    segments, info = model.transcribe(audio_path, beam_size=5)
    # Ghép toàn bộ text
    full_text = "".join([seg.text for seg in segments])
    # Reset generator để đọc lại segments
    segments, _ = model.transcribe(audio_path, beam_size=5)
    result = {
        "text": full_text.strip(),
        "segments": [{"start": seg.start, "end": seg.end, "text": seg.text} for seg in segments],
        "language": info.language
    }
    return result