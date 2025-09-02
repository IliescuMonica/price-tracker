from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

# Set your desired price threshold
BUY_PRICE = 1900

# URL of the product page to track
ninja_url = "https://www.ninja.ro/cuptor-electric-afumator-woodfire-pro-connect-xl-og901eu-7-functii"

# HTTP headers to mimic a browser request
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"}

# Send GET request to fetch the page
response = requests.get(ninja_url,headers=headers,timeout=10)
response.raise_for_status()
web_page = response.text

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(web_page, "html.parser")

# Find the price element and clean it
price = soup.find(class_="pretSale portocaliu").get_text().strip()
price_without_currency = price.split("lei")[0].strip()
price_as_float = float(price_without_currency.replace(".", "").replace(",", "."))

# Find the product title
product = soup.find("h1", class_ = "h1-mobile hidden-md hidden-lg")
product_name = product.get_text()

# Load environment variables for email credentials
load_dotenv()
my_email = os.getenv("MY_EMAIL")
password = os.getenv("MY_EMAIL_PASSWORD")

# Create the email message
msg = f"Subject: Price Alert!\n\n{product_name} is now {price}.\n{ninja_url}"
msg_bytes = msg.encode("utf-8") # Encode to UTF-8 to handle special characters



# Send email if the current price is below the threshold
if price_as_float < BUY_PRICE :
    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg= msg_bytes)