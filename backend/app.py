import os
from datetime import datetime, timezone
from typing import Optional

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from api.rss import RSS_FEEDS, fetch_rss_feed

load_dotenv()

app = FastAPI(
    title="NEWSINTEL AI API",
    version="1.0.0",
    description="Backend proxy for NEWSINTEL AI and NewsAPI."
)

# Development-friendly CORS. For production, replace "*" with your frontend origin.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "").strip()
NEWS_API_URL = "https://newsapi.org/v2/everything"


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "NEWSINTEL AI Backend",
        "time_utc": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "news_api_key_configured": bool(NEWS_API_KEY)
    }

@app.get("/api/rss")
def get_rss():

    all_articles = []

    for source in RSS_FEEDS.values():

        try:
            articles = fetch_rss_feed(
                source["name"],
                source["url"]
            )

            all_articles.extend(articles)

        except Exception as e:
            print(
                f"Gagal mengambil RSS "
                f"{source['name']}: {e}"
            )

    return {
        "status": "success",
        "totalResults": len(all_articles),
        "articles": all_articles
    }

@app.get("/api/news")
def get_news(
    q: str = Query("", min_length=1, max_length=300),
    language: str = Query("id", pattern="^[a-z]{2}$"),
    page_size: int = Query(100, ge=1, le=100),
    sort_by: str = Query("publishedAt", pattern="^(publishedAt|relevancy|popularity)$"),
    page: int = Query(1, ge=1, le=100),
    from_date: Optional[str] = Query(None, alias="from"),
    to_date: Optional[str] = Query(None, alias="to"),
):
    if not NEWS_API_KEY:
        return {
            "status": "error",
            "code": "MISSING_API_KEY",
            "message": "NEWS_API_KEY belum dikonfigurasi di file .env."
        }

    params = {
        "q": q,
        "language": "id",
        "pageSize": page_size,
        "page": page,
        "sortBy": sort_by,
    }

    if from_date:
        params["from"] = from_date
    if to_date:
        params["to"] = to_date

    headers = {"X-Api-Key": NEWS_API_KEY}

    try:
        response = requests.get(
            NEWS_API_URL,
            params=params,
            headers=headers,
            timeout=20
        )
    except requests.exceptions.Timeout:
        return {
            "status": "error",
            "code": "UPSTREAM_TIMEOUT",
            "message": "NewsAPI terlalu lama merespons."
        }
    except requests.exceptions.RequestException as exc:
        return {
            "status": "error",
            "code": "UPSTREAM_REQUEST_ERROR",
            "message": str(exc)
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status": "error",
            "code": "INVALID_UPSTREAM_RESPONSE",
            "message": f"NewsAPI mengembalikan HTTP {response.status_code}."
        }

    if response.status_code != 200 or data.get("status") != "ok":
        return {
            "status": "error",
            "code": data.get("code", f"HTTP_{response.status_code}"),
            "message": data.get("message", "NewsAPI request gagal."),
        }

    articles = []
    for item in data.get("articles", []):
        source = item.get("source") or {}
        articles.append({
            "title": item.get("title") or "Untitled",
            "description": item.get("description") or "",
            "content": item.get("content") or "",
            "url": item.get("url") or "",
            "image": item.get("urlToImage") or "",
            "publishedAt": item.get("publishedAt") or "",
            "source": {
                "id": source.get("id"),
                "name": source.get("name") or "Unknown Source"
            },
            "author": item.get("author") or ""
        })

    return {
        "status": "success",
        "totalResults": data.get("totalResults", 0),
        "articles": articles
    }
