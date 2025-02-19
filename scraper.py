import requests
import feedparser
import json
from datetime import datetime

class NewsScraper:
    def __init__(self):
        self.keywords = {
            "religious": ["hindutva", "tensions", "violence", "riots", "islamophobia"],
            "caste": ["dalit", "supremacy", "reservation", "obc", "privilege"],
            "ideological": ["left-wing", "right-wing", "bjp", "rss", "propaganda"]
        }
        self.rss_feeds = {
            "The Times of India": "https://timesofindia.indiatimes.com/rss.cms",
            "The Hindu": "https://www.thehindu.com/rssfeeds/",
            "The Indian Express": "https://indianexpress.com/feeds/",
            "Hindustan Times": "https://www.hindustantimes.com/rss",
            "The Economic Times": "https://economictimes.indiatimes.com/rss.cms"
        }
        self.up_cities = [
            "Lucknow", "Kanpur", "Varanasi", "Agra", "Allahabad", "Prayagraj", "Ghaziabad", "Noida",
            "Aligarh", "Meerut", "Bareilly", "Gorakhpur", "Saharanpur", "Ayodhya", "Faizabad",
            "Moradabad", "Firozabad", "Jhansi", "Rampur", "Muzaffarnagar", "Shahjahanpur", "Mathura"
        ]
        self.start_date = datetime(2019, 1, 1)
        self.end_date = datetime(2024, 12, 31)

    def fetch_news(self, rss_url):
        response = requests.get(rss_url)
        if response.status_code == 200:
            feed = feedparser.parse(response.text)
            filtered_news = []

            for entry in feed.entries:
                if hasattr(entry, "published"):
                    try:
                        published_date = datetime(*entry.published_parsed[:6])
                        if self.start_date <= published_date <= self.end_date:
                            filtered_news.append({
                                "title": entry.title,
                                "link": entry.link,
                                "date": published_date.strftime("%Y-%m-%d")
                            })
                    except Exception:
                        continue

            return filtered_news
        return []

    def scrape_all_news(self):
        all_news = {}
        for category, keywords in self.keywords.items():
            all_news[category] = {}
            for keyword in keywords:
                all_news[category][keyword] = []
                for source, rss_url in self.rss_feeds.items():
                    news_items = self.fetch_news(rss_url)
                    filtered_news = [item for item in news_items if keyword.lower() in item['title'].lower()]
                    
                    # Further filter by Uttar Pradesh cities/districts
                    up_specific_news = [item for item in filtered_news if any(city in item['title'] for city in self.up_cities)]
                    
                    all_news[category][keyword].extend(up_specific_news)
        return all_news

# Run the scraper
scraper = NewsScraper()
news_data = scraper.scrape_all_news()

# Save news to a JSON file
with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, indent=4, ensure_ascii=False)

print("\nNews data saved to news_data.json")

