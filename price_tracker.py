import requests
from bs4 import BeautifulSoup
import csv

url = "http://books.toscrape.com/"

# 1. Get the HTML
response = requests.get(url)

# --- ADD THIS LINE ---
response.encoding = "utf-8"
# ----------------------

soup = BeautifulSoup(response.text, "html.parser")

print(" --- 📚 BOOK PRICE TRACKER ---")

# 2. Find ALL elements that look like a book
# On this website, every book is inside an <article> tag with class "product_pod"
all_books = soup.find_all("article", class_="product_pod")

# 3. Open a CSV file to save results
with open("book_prices.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Book Title", "Price"]) # Header

    # 4. Loop through each book and extrace details
    for book in all_books:
        # Extract Title: It's inside the <a> tag inside <h3>  
        title = book.h3.find('a')["title"] 

        # Extract Price: It's inside a <p> tag with class "price_color"
        price_text = book.find("p", class_="price_color").text

        # Clean the price(Remove the weird character '£')
        # price = price_text.replace("£", "").replace("Â", "")
        price = price_text.replace("£", "")

        # Print to terminal
        print(f"found: {title} - {price}")

        # Save to file
        writer.writerow([title, price])

print("--- ✅ DONE! Data saved to 'book_prices.csv' ---")

    