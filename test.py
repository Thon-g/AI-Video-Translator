import asyncio
import re
from ollama import chat, ChatResponse

from get_transcript import get_transcript
from language_map import language_map
from translate_transcript import translate_segments


def clean_translation(text):
    # Xóa tất cả thẻ <think>...</think>
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()

def split_sentences(text):
    sentence_end_re = re.compile(r'(?<=[.!?…])\s+')
    list_text = [s.strip() for s in sentence_end_re.split(text)]
    # bỏ các giá trị thừa
    list_text = [text for text in list_text if text]
    return list_text


# text = """
# Don't go to Vietnam without learning these 5 simple street food tips.
# First, the elephant in the room. Will you get food poisoning? The short answer is probably not. We've lived here for 2 years and we haven't had issues with things like raw vegetables or ice and drinks. If a street food stall is filled with locals, 9 times out of 10 you'll be fine. The cheapest drink you can order at virtually any restaurant or street food in Vietnam is called Chhada or Ice Tea. It's often free at smaller vendors or up to 20 cents per cup. Sometimes you'll already find it on the table or you can find it tucked away for you to freely take yourself like this but we always ask first. If you see this on the table, it's homemade chili paste. This stuff is deadly. Beware and start with a bit. If you see these wipes served to you, they're not free. It's 20 cents to 40 cents per wipe which is cheap but worth noting if you see it on your bill when you're finished eating. If you have limes on your table, use them to wipe your chopsticks. They're generally clean but it's better to be safe from sorry. We live in Vietnam and post content like this daily. So give us a follow if you're planning a trip.
# """

# list_text = split_sentences(text)
#
# list_translated = asyncio.run(translate_segments(list_text, 'en', 'vi'))
#
# for tran in list_translated:
#     print(tran)

# import whisper
#
# vocals_path = "split_temp\\vocals.wav"
# transcript = get_transcript(vocals_path)
#
# segments = transcript["segments"]
#
# for i,seg in enumerate(segments):
#     print(f"{i}. start: {seg['start']} - duration: {float(seg['end'] - seg['start'])} - text: {seg['text']}")


# vocals_path = "split_temp\\vocals.wav"
# target_lang_code = "vi"
# print("lấy trascript")
# result = get_transcript(vocals_path)
# segments = result["segments"]
# print("segments:")
# for seg in segments:
#     print(seg["text"])
#
# print("dịch transcirpt và trả về dict translated")
# segments = result["segments"]
# orin_lang_code = result["language"]
# translated = asyncio.run(translate_segments(segments, orin_lang_code, target_lang_code))
# print(f"translate:")
# for seg in translated:
#     print(seg["text"])

text = """
I wake up early in the morning.
The sun is shining through my window.
I brush my teeth and wash my face.
Then, I prepare a cup of coffee.
After breakfast, I start my work on the computer.
At noon, I take a short break and eat lunch.
In the afternoon, I continue working until evening.
Finally, I relax by reading a book before going to bed.
"""
list_text = [t.strip() for t in text.splitlines() if t.strip()]
# print(list_text)



def chatQwen3(segments, origin_lang_code, target_lang_code):
    list_text = [seg['text'].strip() for seg in segments if seg['text'].strip()]
    origin_lang = language_map[origin_lang_code]
    target_lang = language_map[target_lang_code]
    if origin_lang_code == target_lang_code:
        return segments

    system_prompt = f"""
    You are a translation engine. 
    Your ONLY task is to translate text from {origin_lang} into {target_lang}. 
    DO NOT output {origin_lang}, DO NOT detect language, and DO NOT output anything except {target_lang} translations. 
    Constraints:
    - Output must contain exactly {len(list_text)} lines.
    - Each input sentence = exactly one output sentence, in the same order.
    - Do not merge or split sentences.
    - Do not explain or add extra text.
    - Output only the translations in {target_lang}, one per line.
    - Each translation must be as short and concise as possible, like subtitles.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"/set_nothink {list_text} /set_nothink"}
    ]

    response: ChatResponse = chat(model='qwen3:latest', messages=messages)

    result = clean_translation(response['message']['content'])
    translated_lines = result.splitlines()

    # nếu thiếu dòng -> fill bằng chuỗi rỗng hoặc copy lại gốc
    if len(translated_lines) < len(list_text):
        translated_lines += [""] * (len(list_text) - len(translated_lines))

    # nếu thừa dòng -> cắt bớt
    translated_lines = translated_lines[:len(list_text)]

    translated = []
    for seg, new_text in zip(segments, translated_lines):
        translated.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": new_text.strip()
        })
    return translated


# vocals_path = "split_temp\\vocals.wav"
#
# result = get_transcript(vocals_path)
# print(f"result = {result}")
#
# print("dịch transcirpt và trả về dict translated")
# segments = result["segments"]
# orin_lang_code = result["language"]
# translated = translate_segments(segments, orin_lang_code, "vi")
#
# print(f"{translated}")