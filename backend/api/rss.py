import feedparser

RSS_FEEDS = {
    # =========================
    # ANTARA NASIONAL
    # =========================
    "antara_terkini": {
        "name": "ANTARA Terkini",
        "url": "https://www.antaranews.com/rss/terkini.xml"
    },

    "antara_top": {
        "name": "ANTARA Top News",
        "url": "https://www.antaranews.com/rss/top-news.xml"
    },

    "antara_politik": {
        "name": "ANTARA Politik",
        "url": "https://www.antaranews.com/rss/politik.xml"
    },

    "antara_hukum": {
        "name": "ANTARA Hukum",
        "url": "https://www.antaranews.com/rss/hukum.xml"
    },

    "antara_ekonomi": {
        "name": "ANTARA Ekonomi",
        "url": "https://www.antaranews.com/rss/ekonomi.xml"
    },

    # =========================
    # ANTARA JABAR
    # =========================
    "antara_jabar": {
        "name": "ANTARA Jabar",
        "url": "https://jabar.antaranews.com/rss/terkini.xml"
    },

    # =========================
    # ANTARA MEGAPOLITAN
    # =========================
    "antara_megapolitan": {
        "name": "ANTARA Megapolitan",
        "url": "https://megapolitan.antaranews.com/rss/terkini.xml"
    },

    # =========================
    # CNA INDONESIA
    # =========================
    "cna_indonesia": {
        "name": "CNA Indonesia",
        "url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml"
    },

    "cna_dunia": {
        "name": "CNA Dunia",
        "url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml&category=3136"
    },

    "cna_bisnis": {
        "name": "CNA Bisnis",
        "url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml&category=3321"
    }
}

def fetch_rss_feed(feed_name, feed_url):

    feed = feedparser.parse(feed_url)

    articles = []

    for entry in feed.entries:

        articles.append({
            "title": entry.get("title", ""),
            "description": entry.get("summary", ""),
            "url": entry.get("link", ""),
            "publishedAt": entry.get("published", ""),
            "source": {
                "name": feed_name
            },
            "author": entry.get("author", ""),
            "image": ""
        })

    return articles