import os
from datetime import datetime
import edge_tts
import asyncio
import subprocess
from concurrent.futures import ThreadPoolExecutor


def init_output_dir():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outputDir = f"temp_{now}"
    os.makedirs(outputDir, exist_ok=True)
    return outputDir


# Semaphore giới hạn số TTS chạy đồng thời (tránh bị rate-limit)
TTS_CONCURRENCY = 5

async def speak(index, text, outputDir, voice, semaphore):
    async with semaphore:
        filePath = os.path.join(outputDir, f"{index}.mp3")
        communicate = edge_tts.Communicate(text, voice=voice, rate="+20%")
        await communicate.save(filePath)


async def text_to_speech(listText, voice):
    # tạo folder lưu file audio
    outputDirAudio = init_output_dir()
    # TTS song song với semaphore giới hạn concurrent
    semaphore = asyncio.Semaphore(TTS_CONCURRENCY)
    tasks = [
        speak(i, text, outputDirAudio, voice, semaphore)
        for i, text in enumerate(listText)
    ]
    await asyncio.gather(*tasks)

    return outputDirAudio


def _convert_single(mp3_path, wav_path):
    """Convert 1 file mp3 -> wav rồi xóa mp3."""
    subprocess.run(
        ["ffmpeg", "-y", "-i", mp3_path, "-ar", "24000", wav_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )
    os.remove(mp3_path)


def convertMp3ToWav(outputDirAudio):
    """Convert tất cả mp3 -> wav song song bằng ThreadPoolExecutor."""
    convert_jobs = []
    for file in os.listdir(outputDirAudio):
        if file.endswith(".mp3"):
            mp3_path = os.path.join(outputDirAudio, file)
            wav_path = os.path.join(outputDirAudio, os.path.splitext(file)[0] + ".wav")
            convert_jobs.append((mp3_path, wav_path))

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(_convert_single, mp3, wav) for mp3, wav in convert_jobs]
        for f in futures:
            f.result()  # chờ tất cả xong + raise nếu có exception