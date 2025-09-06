import csv
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC    
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re

def safe_float(text):
    """Convert price string like '$237' to float. Return None if empty/invalid."""
    if text:
        cleaned = text.replace("$", "").replace(",", "").strip()
        return float(cleaned) if cleaned else None
    return None

# Setup Selenium and WebDriver
chrome_option = Options()
chrome_option.add_argument('--headless')
chrome_option.add_argument('--disable-gpu')
chrome_option.add_argument('--no-sandbox')
chrome_option.add_argument('--disable-dev-shm-usage')
chrome_option.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.265 Safari/537.36"
)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_option)

url = "https://www.framesdirect.com/eyeglasses"
print(f"Visiting {url} page")
driver.get(url)

# Wait for product tiles to load
try:
    WDW(driver, 15).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'prod-holder'))
    )
except TimeoutException:
    print("Timed out waiting for products to load")
    driver.quit()
    exit(1)

# Parse page source
content = driver.page_source
page = BeautifulSoup(content, 'html.parser')

glasses_data = []

product_holder = page.find_all("div", class_='prod-holder')
print(f"Found {len(product_holder)} products")

for tile in product_holder:
    # --- Product title section ---
    prod_title = tile.find("div", class_='prod-title prod-model')
    
    if prod_title:
        brand_tag = prod_title.find("div", class_='catalog-name')  
        brand = brand_tag.get_text(strip=True) if brand_tag else None

        product_name = prod_title.find("div", class_='product_name')
        name = product_name.get_text(strip=True) if product_name else None
    else:
        brand = name = None

    # --- Price Section ---
    price_wrap = tile.find("div", class_='prod-price-wrap')
    if price_wrap:
        current_price_tag = price_wrap.find("div", class_='prod-aslowas')
        current_price = safe_float(current_price_tag.get_text(strip=True)) if current_price_tag else None

        former_price_tag = price_wrap.find("div", class_='prod-catalog-retail-price')
        former_price = safe_float(former_price_tag.get_text(strip=True)) if former_price_tag else None

        discount_tag = price_wrap.find("div", class_='frame-discount')
        if discount_tag:
            discount_text = discount_tag.get_text(strip=True)
            match = re.search(r"(\d+)", discount_text)
            discount = float(match.group(1)) if match else None
        else:
            discount = None
    else:
        former_price = current_price = discount = None
    
    # Always append, even if some fields are None
    glasses_data.append({
        "brand": brand,
        "name": name,
        "current_price": current_price,
        "former_price": former_price,
        "discount": discount
    })

# --- Export to CSV ---
import csv
with open("eyeglasses_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["brand", "name", "current_price", "former_price", "discount"])
    writer.writeheader()
    writer.writerows(glasses_data)

print(f"Extracted {len(glasses_data)} products and saved to eyeglasses_data.csv")

# Save to JSON
# Save to JSON
with open("data/glassesdotcom.json", mode='w', encoding='utf-8') as json_file:
        json.dump(glasses_data, json_file, indent=4, ensure_ascii=False)
print(f"Saved {len(glasses_data)} records to JSON")

# Close the browser
driver.quit()
print("End of Web Extraction")