import feedparser

RSS_FEEDS = {
    "antara": {
        "name": "ANTARA",
        "url": "https://www.antaranews.com/rss/terkini.xml"
    },
    "antara_top": {
        "name": "ANTARA Top News",
        "url": "https://www.antaranews.com/rss/top-news.xml"
    },
    "cna": {
        "name": "CNA Indonesia",
        "url": "https://www.cna.id/api/v1/rss-outbound-feed?_format=xml"
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