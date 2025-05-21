import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse

# List of product URLs
URLS = [
    "https://cookinglife.nl/products/cookinglife-serviesset-summer-vibes",
    "https://cookinglife.nl/products/cookinglife-drankdispenser-met-houder-4liter",
    "https://cookinglife.nl/products/schott-zwiesel-wijnglazenset-fortissimo-18-delig",
    "https://cookinglife.nl/products/coravin-sparkling-pack-wijn-conserveringssysteem-zwart",
    "https://cookinglife.nl/products/sola-pannenset-pearl-7-delig"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Directory to save JSON files
OUTPUT_DIR = "CookingLife_Prototype"

def scrape_product(url):
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"❌ Failed to load page: {url}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Extract product title
    title_tag = soup.find("h1")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown Product"

    # Extract features from the 'Kenmerken' section
    features = {}
    kenmerken_section = soup.find("section", id="product-details")
    if kenmerken_section:
        rows = kenmerken_section.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                features[key] = value

    # Extract dimensions and number of items
    dimensions = {}
    items_included = {}
    for key, value in features.items():
        if "lengte" in key.lower() or "breedte" in key.lower() or "hoogte" in key.lower() or "inhoud" in key.lower():
            dimensions[key] = value
        if "stuks" in key.lower() or "inhoud doos" in key.lower():
            items_included[key] = value

    # Prepare data dictionary
    data = {
        "title": title,
        "dimensions": dimensions,
        "items_included": items_included,
        "features": features
    }

    # Generate filename from URL slug
    slug = os.path.basename(urlparse(url).path)
    filename = f"{slug}.json"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save data to JSON file
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved data for '{title}' to {filepath}")

def main():
    for url in URLS:
        scrape_product(url)

if __name__ == "__main__":
    main()