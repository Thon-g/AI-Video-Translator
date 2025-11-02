# AI-Video-Translator
Automatically translate and dub any video or YouTube URL into another language.

## Giới thiệu
Dự án này cho phép:
- Tải video từ YouTube hoặc upload file.
- Tách audio và video.
- Dịch transcript sang nhiều ngôn ngữ.
- Chuyển văn bản sang giọng nói (TTS).
- Ghép lại video với audio đã dịch.

## Cài đặt
1. Clone repo:
git clone https://github.com/username/repo.git
cd repo

2.Tạo virtual environment:
python -m venv .venv

3.Cài dependencies:
pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu124

6.Cấu hình
Nếu có config hoặc API key:
```markdown
## Cấu hình
- Mở `config.py` và điền các API key:
```python
TRANSLATION_PROVIDER = "gemini"
GEMINI_API_KEY = "your_api_key"
GEMINI_MODEL = "gemini-2.5-flash"

##Cách sử dụng
```bash
streamlit run GUI.py
