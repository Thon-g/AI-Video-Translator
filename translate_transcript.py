import re
import time
from language_map import language_map
import config
from ollama import chat as ollama_chat, ChatResponse as OllamaResponse

def clean_translation(text):
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    return text.strip()


def translate_segments(segments, origin_lang_code, target_lang_code):
    t0 = time.time()
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

    # --- Chọn provider ---
    provider = config.TRANSLATION_PROVIDER.lower()

    if provider == "ollama":
        from ollama import chat as ollama_chat
        model = config.OLLAMA_MODEL
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n".join(list_text)}
        ]
        response = ollama_chat(model=model, messages=messages)
        raw_text = response['message']['content']

    elif provider == "openai":
        import openai
        openai.api_key = config.OPENAI_API_KEY
        model = config.OPENAI_MODEL
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "\n".join(list_text)}
        ]
        completion = openai.chat.completions.create(model=model, messages=messages)
        raw_text = completion.choices[0].message.content


    elif provider == "gemini":
        from google import genai
        client = genai.Client(api_key=config.GEMINI_API_KEY)
        model = config.GEMINI_MODEL
        prompt_text = system_prompt + "\n" + "\n".join(list_text)
        response = client.models.generate_content(
            model=model,
            contents=[prompt_text]
        )
        raw_text = response.text

    else:
        raise ValueError(f"Provider {provider} chưa được hỗ trợ!")

    result = clean_translation(raw_text)
    translated_lines = result.splitlines()

    # Nếu thiếu dòng, bổ sung ""
    if len(translated_lines) < len(list_text):
        translated_lines += [""] * (len(list_text) - len(translated_lines))

    # Nếu thừa dòng -> cắt bớt
    translated_lines = translated_lines[:len(list_text)]

    translated = []
    for seg, new_text in zip(segments, translated_lines):
        translated.append({
            "start": seg["start"],
            "end": seg["end"],
            "text": new_text.strip()
        })

    t1 = time.time()
    print(f"Thời gian dịch: {t1 - t0:.2f}s")
    return translated



# def translate_segments(segments, origin_lang_code, target_lang_code):
#     t0 = time.time()
#     list_text = [seg['text'].strip() for seg in segments if seg['text'].strip()]
#     origin_lang = language_map[origin_lang_code]
#     target_lang = language_map[target_lang_code]
#     if origin_lang_code == target_lang_code:
#         return segments
#
#     system_prompt = f"""
#     You are a translation engine.
#     Your ONLY task is to translate text from {origin_lang} into {target_lang}.
#     DO NOT output {origin_lang}, DO NOT detect language, and DO NOT output anything except {target_lang} translations.
#     Constraints:
#     - Output must contain exactly {len(list_text)} lines.
#     - Each input sentence = exactly one output sentence, in the same order.
#     - Do not merge or split sentences.
#     - Do not explain or add extra text.
#     - Output only the translations in {target_lang}, one per line.
#     - Each translation must be as short and concise as possible, like subtitles.
#     """
#
#     messages = [
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": f"/set_nothink {list_text} /set_nothink"}
#     ]
#
#     response: ChatResponse = chat(model='qwen3', messages=messages)
#
#     result = clean_translation(response['message']['content'])
#     translated_lines = result.splitlines()
#
#     if len(translated_lines) < len(list_text):
#         translated_lines += [""] * (len(list_text) - len(translated_lines))
#
#     # nếu thừa dòng -> cắt bớt
#     translated_lines = translated_lines[:len(list_text)]
#
#     translated = []
#     for seg, new_text in zip(segments, translated_lines):
#         translated.append({
#             "start": seg["start"],
#             "end": seg["end"],
#             "text": new_text.strip()
#         })
#
#     t1= time.time()
#     print(f"thời gian dịch là: {t1 - t0}")
#     return translated



# async def translate_segments(segments, origin_lang_code, target_lang_code):
#     translator = Translator()
#     origin_lang = language_map[origin_lang_code]
#     target_lang = language_map[target_lang_code]
#
#     translated = []
#     t0 = time.time()
#     for seg in segments:
#         text = seg["text"]
#         if text.strip():
#             result = await translator.translate(text, src=origin_lang, dest=target_lang)
#             translated_text = result.text
#             translated.append({
#                 "start": seg["start"],
#                 "end": seg["end"],
#                 "text": translated_text
#             })
#     t1 = time.time()
#     print(f"thời gian dịch = {round(t1-t0,2)}")
#
#     return translated

# def translate_segments2(segments, origin_lang_code, target_lang_code):
#     local = r"D:\Model\Translate\nllb-200-distilled-1.3B"
#     device = 0 if torch.cuda.is_available() else -1
#
#     orin_lang = facebook_lang_map[origin_lang_code]
#     target_lang = facebook_lang_map[target_lang_code]
#
#     tokenizer = AutoTokenizer.from_pretrained(local, src_lang=orin_lang)
#     model = AutoModelForSeq2SeqLM.from_pretrained(local)
#     if torch.cuda.is_available():
#         model = model.to("cuda").half()
#
#     translator = pipeline("translation", model=model, tokenizer=tokenizer, device=device)
#
#     # gom tất cả câu gốc
#     list_text = [seg["text"] for seg in segments if seg["text"].strip()]
#
#     t0 = time.time()
#     # dịch toàn bộ list_text trong 1 lần
#     outputs = translator(list_text, src_lang=orin_lang, tgt_lang=target_lang, max_length=1024)
#     t1 = time.time()
#
#     # ghép kết quả dịch vào lại segments
#     translated = []
#     j = 0
#     for seg in segments:
#         if not seg["text"].strip():
#             continue
#         out_text = outputs[j]["translation_text"] if isinstance(outputs[j], dict) else outputs[j]
#         translated.append({
#             "start": seg["start"],
#             "end": seg["end"],
#             "text": out_text
#         })
#         j += 1
#
#     print(f"len(list_text) = {len(list_text)}")
#     print(f"len(trans) = {len(translated)}")
#     print(f"thời gian dịch = {round(t1-t0,2)}")
#
#     return translated