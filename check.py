import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import time
import subprocess

# Phrase to look for on the websites
target_phrase = "Out of Stock"

# Email settings
email = "contact@dambshop.com"
to_email = "abdelilahazilal043@gmail.com"
smtp_server = "smtp-pulse.com"
smtp_port = 587
smtp_password = "oTHcGJbJ5rdQPj"


# Loop indefinitely
while True:
    # List of websites to scrape
    urls = ['https://www.calvetsupply.com/capsules-and-tablets-fish-aid-antibiotics.html',
            'https://www.calvetsupply.com/Capsules-Powders-and-Tablets_c_330-2.html'] # Replace with the URL of the webpage you want to scrape

    for url in urls:
        # Make GET request using curl
        command = ['curl', '-s', url]
        response = subprocess.check_output(command, universal_newlines=True)

        # Parse response as HTML
        soup = BeautifulSoup(response, 'html.parser')

        names = soup.find_all(class_='name')

        for name in names:
            link = name.find('a')
            if link:
                # Make GET request to individual product page using curl
                product_url = "https://www.calvetsupply.com/" + link['href']
                command = ['curl', '-s', product_url]
                product_response = subprocess.check_output(command, universal_newlines=True)

                product_soup = BeautifulSoup(product_response, "html.parser")
                content = product_soup.get_text()
                title = product_soup.title.string

                # Check if the target phrase is in the website content or title
                if target_phrase in content or target_phrase in title:
                    # Send email alert
                    message = f"Subject: {title} is out of stock"
                    msg = MIMEText(message)
                    msg['From'] = email
                    msg['To'] = to_email
                    print(f"{title} is out of stock")

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(to_email, smtp_password)
                        server.sendmail(email, to_email, msg.as_string())
                else:
                    print()
                    print(f"{title} is available")
                    print()

    # Wait for 10 minutes before checking again
    time.sleep(500)
    print("===========================================================")
    print(datetime)
    print("===========================================================")
