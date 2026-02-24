import requests
from bs4 import BeautifulSoup
import csv
import random 

url = "http://books.toscrape.com/"

# --- List of fake browser ID badges (User-Agents) ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
]

# Randomly pick one User-Agent from the list
random_agent = random.choice(USER_AGENTS)

# Package it into a "Headers" dictionary to send to the website
headers = {
    "User-Agent": random_agent
}

print(f"🕵️ Disguising script as: {random_agent[:50]}...")

# 1. Get the HTML (Passing the headers to bypass anti-bot detection)
response = requests.get(url, headers=headers)
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

print(" --- 📚 BOOK PRICE TRACKER ---")

# 2. Find ALL elements that look like a book
all_books = soup.find_all("article", class_="product_pod")

# 3. Open a CSV file to save results
with open("book_prices.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Book Title", "Price"]) # Header

    # 4. Loop through each book and extract details
    for book in all_books:
        title = book.h3.find('a')["title"] 
        price_text = book.find("p", class_="price_color").text
        price = price_text.replace("£", "")

        print(f"Found: {title} - {price}")
        writer.writerow([title, price])

print("--- ✅ DONE! Data saved to 'book_prices.csv' ---")