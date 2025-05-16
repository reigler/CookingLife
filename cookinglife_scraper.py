import os
import requests
from bs4 import BeautifulSoup
import json

# Target product URL
URLS = [
    "https://cookinglife.nl/products/cookinglife-citruspers",
    "https://cookinglife.nl/products/cookinglife-drankdispenser-2-4liter"
]
HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Path to write the JSON into the frontend folder
USP_JSON_PATH = "CookingLife_Prototype/usps.json"

def scrape_usps():
    response = requests.get(URL, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Failed to load page: {response.status_code}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    section = soup.find("section", class_="col content mb-0 mb-md-3")
    if not section:
        print("❌ Could not find content section.")
        return

    usps = []
    for ul in section.find_all("ul"):
        for li in ul.find_all("li"):
            strong_tags = li.find_all("strong")
            for tag in strong_tags:
                text = tag.get_text(strip=True)
                if text:
                    usps.append(text)

    if usps:
        os.makedirs(os.path.dirname(USP_JSON_PATH), exist_ok=True)
        with open(USP_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(usps, f, ensure_ascii=False, indent=2)
        print(f"✅ Saved {len(usps)} USPs to {USP_JSON_PATH}")
    else:
        print("⚠️ No USPs found.")

if __name__ == "__main__":
    scrape_usps()