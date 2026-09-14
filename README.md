# NEWSINTEL AI — Realtime News

## Struktur

```text
NEWSINTEL_AI/
├── backend/
│   ├── app.py
│   ├── .env
│   └── requirements.txt
└── frontend/
    └── index.html
```

## 1. Konfigurasi API Key

Edit `backend/.env`:

```env
NEWS_API_KEY=API_KEY_BARU_DARI_NEWSAPI
```

Jangan commit `.env` ke GitHub dan jangan masukkan API key ke HTML.

## 2. Install

Windows PowerShell:

```powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 3. Jalankan backend

```powershell
uvicorn app:app --reload
```

Backend:
`http://127.0.0.1:8000`

Health check:
`http://127.0.0.1:8000/api/health`

## 4. Buka frontend

Buka `frontend/index.html` di browser.

Frontend akan meminta data ke:

```text
http://127.0.0.1:8000/api/news
```

## Catatan

Versi ini menggunakan NewsAPI sebagai sumber berita dan melakukan analisis intelligence ringan di browser. Untuk production, API key tetap di backend dan CORS sebaiknya dibatasi ke domain frontend.
