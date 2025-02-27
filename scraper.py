import requests
import feedparser
import json

class NewsScraper:
    def __init__(self):
        self.keywords = {
            "religious": ["hindutva", "tensions", "violence", "riots", "islamophobia", "communal", "extremism", "mob lynching"],
            "caste": ["dalit", "supremacy", "reservation", "obc", "privilege", "sc/st", "discrimination", "quota"],
            "ideological": ["left-wing", "right-wing", "bjp", "rss", "propaganda", "communism", "fascism", "liberal", "conservative"]
        }
        self.rss_feeds = {
            "The Hindu": [
                "https://www.thehindu.com/news/national/feeder/default.rss",
                "https://www.thehindu.com/news/international/feeder/default.rss"
            ],
            "The Indian Express": [
                "https://indianexpress.com/section/india/feed/",
                "https://indianexpress.com/section/world/feed/"
            ],
            "Hindustan Times": [
                "https://www.hindustantimes.com/feeds/rss/india-news/rssfeed.xml",
                "https://www.hindustantimes.com/feeds/rss/world-news/rssfeed.xml"
            ],
            "Google News": [
                "https://news.google.com/rss/search?q=India",
                "https://news.google.com/rss/search?q=Politics+India",
                "https://news.google.com/rss/search?q=Violence+India"
            ]
        }
    
    def fetch_news(self, rss_urls):
        all_entries = []
        for rss_url in rss_urls:
            response = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"})
            if response.status_code == 200:
                feed = feedparser.parse(response.text)
                all_entries.extend([{"title": entry.title, "link": entry.link} for entry in feed.entries])
        return all_entries

    def scrape_all_news(self):
        all_news = {}
        for category, keywords in self.keywords.items():
            all_news[category] = {}
            for keyword in keywords:
                all_news[category][keyword] = []
                for source, rss_urls in self.rss_feeds.items():
                    news_items = self.fetch_news(rss_urls)
                    filtered_news = [item for item in news_items if keyword.lower() in item['title'].lower()]
                    all_news[category][keyword].extend(filtered_news)
        return all_news

# Run the scraper
scraper = NewsScraper()
news_data = scraper.scrape_all_news()

# Save news to a JSON file
with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, indent=4, ensure_ascii=False)

print("\nNews data saved to news_data.json")
