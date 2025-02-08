import requests
import feedparser
import json

class NewsScraper:
    def __init__(self):
        self.keywords = {
            "religious": ["hindutva", "tensions", "violence", "riots", "islamophobia"],
            "caste": ["dalit", "supremacy", "reservation", "obc", "privilege"],
            "ideological": ["left-wing", "right-wing", "bjp", "rss", "propaganda"]
        }

    def fetch_news(self, keyword):
        url = f"https://news.google.com/rss/search?q={keyword}"
        response = requests.get(url)
        if response.status_code == 200:
            feed = feedparser.parse(response.text)
            return [{"title": entry.title, "link": entry.link} for entry in feed.entries]
        return []

    def scrape_all_news(self):
        all_news = {}
        for category, keywords in self.keywords.items():
            all_news[category] = {k: self.fetch_news(k) for k in keywords}
        return all_news

# Run the scraper
scraper = NewsScraper()
news_data = scraper.scrape_all_news()

# Save news to a JSON file
with open("news_data.json", "w", encoding="utf-8") as f:
    json.dump(news_data, f, indent=4, ensure_ascii=False)

print("\nNews data saved to news_data.json")
