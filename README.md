# AI-Video-Translator
Tự động dịch và lồng tiếng bất kỳ video hoặc URL YouTube nào sang ngôn ngữ khác.

## Giới thiệu
Dự án này cho phép:
- Tải video từ YouTube hoặc upload file.
- Tách audio và video.
- Dịch transcript sang nhiều ngôn ngữ.
- Chuyển văn bản sang giọng nói (TTS).
- Ghép lại video với audio đã dịch.

## Cài đặt
1. Clone repo:
```bash
git clone https://github.com/Thon-g/AI-Video-Translator.git
cd repo
```

2. Tạo virtual environment:
```bash
python -m venv .venv
```

3. Kích hoạt virtual environment:
- Trên Windows:
```bash
.venv\Scripts\activate
```
- Trên macOS / Linux:
```bash
source .venv/bin/activate
```

4. Cài dependencies:
```bash
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124
```

## Cấu hình
- Mở file `config.py` và điền các API key, model bạn muốn dùng. Ví dụ với Google Gemini:
```python
TRANSLATION_PROVIDER = "gemini"
GEMINI_API_KEY = "your_api_key"
GEMINI_MODEL = "gemini-2.5-flash"
```

- Ví dụ với các provider khác:
```python
# OLLAMA_MODEL = "qwen3"           # Ollama local
# OPENAI_API_KEY = "your_openai_key"
# OPENAI_MODEL = "gpt-4o-mini"
```

## Cách sử dụng
1. Chạy ứng dụng:
```bash
streamlit run GUI.py
```

2. Trong giao diện Streamlit:
- Chọn upload video hoặc nhập URL YouTube.
- Chọn ngôn ngữ cần dịch.
- Chọn giọng đọc TTS.
- Nhấn **Bắt đầu xử lý video** để nhận video đã dịch.

## License
MIT License
