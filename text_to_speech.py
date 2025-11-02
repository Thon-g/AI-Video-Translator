import os
from datetime import datetime
import edge_tts
import asyncio
import subprocess


def init_output_dir():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    outputDir = f"temp_{now}"
    os.makedirs(outputDir, exist_ok=True)
    return outputDir

async def speak(index, text, outputDir, voice = "vi-VN-HoaiMyNeural"):
    filePath = os.path.join(outputDir, f"{index}.mp3")
    communicate = edge_tts.Communicate(text, voice=voice, rate="+20%")
    await communicate.save(filePath)


async def text_to_speech(listText, voice):
    # tạo folder lưu file audio
    outputDirAudio = init_output_dir()
    # cái này tts từng câu trong list
    tasks = []
    for i, text in enumerate(listText):
        if text.strip():    # check ko rỗng
            tasks.append(speak(i, text, outputDirAudio, voice))
    for task in tasks:
        await task
        await asyncio.sleep(0.2)

    return outputDirAudio


def convertMp3ToWav(outputDirAudio):
    # fileList = []
    for file in os.listdir(outputDirAudio):
        if file.endswith(".mp3"):
            mp3_path = os.path.join(outputDirAudio, file)
            wav_path = os.path.join(outputDirAudio, os.path.splitext(file)[0] + ".wav")

            # Convert mp3 -> wav
            subprocess.run([
                "ffmpeg", "-y", "-i", mp3_path,
                "-ar", "24000",
                wav_path
            ])
            # Xóa file mp3 sau khi convert
            os.remove(mp3_path)
            # fileList.append(wav_path)

    # sort theo số thứ tự trong tên file
    # fileList.sort(key=lambda f: int(os.path.splitext(os.path.basename(f))[0]))
    # return fileList