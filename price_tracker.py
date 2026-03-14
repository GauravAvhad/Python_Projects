import requests
from bs4 import BeautifulSoup
import random
import sqlite3
import matplotlib.pyplot as plt

# --- 1. SET UP THE SQLITE DATABASE ---
# This creates a file called 'pricing_data.db' on your computer
conn = sqlite3.connect('pricing_data.db')
cursor = conn.cursor()

# Create a table with two columns: Title (Text) and Price (Decimal Number)
cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                  (title TEXT, price REAL)''')

# Clear out old data so we only see fresh prices every time we run it
cursor.execute('''DELETE FROM products''') 

# --- 2. SCRAPE THE DATA ---
print("Scraping data...")
url = "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
]
headers = {"User-Agent": random.choice(USER_AGENTS)}

response = requests.get(url, headers=headers)

# THE FIX: Force Python to use UTF-8 encoding so it reads the '£' symbol correctly
response.encoding = 'utf-8' 

soup = BeautifulSoup(response.text, "html.parser")
books = soup.find_all("article", class_="product_pod")

# We will just scrape the first 5 books to make our chart look clean
for book in books[:5]:
    title = book.h3.a["title"]
    price_text = book.find("p", class_="price_color").text
    
    # --- 3. CLEAN & STORE IN SQLITE DATABASE ---
    # Because of the utf-8 fix, this will now cleanly strip just the £ symbol
    price_float = float(price_text.replace("£", ""))
    
    cursor.execute('''INSERT INTO products (title, price) 
                      VALUES (?, ?)''', (title, price_float))

# Save (commit) the changes to the database
conn.commit()
print("Data successfully saved to SQLite database!")

# --- 4. VISUALIZE THE DATA ---
print("Generating chart...")
# Retrieve the data back out of the database
cursor.execute('''SELECT title, price FROM products''')
data = cursor.fetchall()

# Separate the data into two lists for the X and Y axes
titles = [row[0][:15] + "..." for row in data] # Shorten titles so they fit on the screen
prices = [row[1] for row in data]

# Draw the Bar Chart
plt.figure(figsize=(10, 6))
plt.bar(titles, prices, color='skyblue')
plt.title("E-Commerce Book Prices")
plt.xlabel("Book Title")
plt.ylabel("Price (£)")
plt.xticks(rotation=45) # Tilt the text so it's easy to read
plt.tight_layout()

# Pop the chart open on your screen!
plt.show()

# Close the database connection
conn.close()