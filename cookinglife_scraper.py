import os
import requests
from bs4 import BeautifulSoup
import json

# Target product URLs
URLS = [
    "https://cookinglife.nl/products/cookinglife-citruspers",
    "https://cookinglife.nl/products/cookinglife-drankdispenser-2-4liter"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_usps():
    for url in URLS:
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            print(f"❌ Failed to load page {url}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        section = soup.find("section", class_="col content mb-0 mb-md-3")
        if not section:
            print(f"❌ Could not find content section for {url}")
            continue

        usps = []
        for ul in section.find_all("ul"):
            for li in ul.find_all("li"):
                strong_tags = li.find_all("strong")
                for tag in strong_tags:
                    text = tag.get_text(strip=True)
                    if text:
                        usps.append(text)

        if usps:
            slug = url.rstrip('/').split('/')[-1]
            json_path = f"CookingLife_Prototype/usps_{slug}.json"
            os.makedirs(os.path.dirname(json_path), exist_ok=True)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(usps, f, ensure_ascii=False, indent=2)
            print(f"✅ Saved {len(usps)} USPs to {json_path}")
        else:
            print(f"⚠️ No USPs found for {url}")

if __name__ == "__main__":
    scrape_usps()