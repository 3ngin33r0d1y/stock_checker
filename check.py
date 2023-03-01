from datetime import datetime

import requests
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import time





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
    # Scrape each website in the list
    urls = ['https://www.calvetsupply.com/capsules-and-tablets-fish-aid-antibiotics.html', 'https://www.calvetsupply.com/Capsules-Powders-and-Tablets_c_330-2.html'] # Replace with the URL of the webpage you want to scrape

    for url in urls:
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

        names = soup.find_all(class_='name')
        # List of websites to scrape
        websites = []

        for name in names:
            link = name.find('a')
            if link:
                #print("https://www.calvetsupply.com/" + link['href'])

                response = requests.get("https://www.calvetsupply.com/" + link['href'])
                soup = BeautifulSoup(response.content, "html.parser")
                content = soup.get_text()
                title = soup.title.string

                # Check if the target phrase is in the website content or title
                if target_phrase in content or target_phrase in title:
                    # Send email alert
                    message = f"Subject: {link['href']} IS OUT OF STOCK"
                    msg = MIMEText(message)
                    msg['From'] = email
                    msg['To'] = to_email
                    #print('https://www.calvetsupply.com/' + link + " \t is \t" + target_phrase)
                    print(f" {link['href'] } is out of stock ")
                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(to_email, smtp_password)
                        server.sendmail(email, to_email, msg.as_string())
                else:
                     print(f"{title} in stock")
                   

    # Wait for 10 minutes before checking again
    time.sleep(3600)
    print("===========================================================")
    print(datetime)
    print("===========================================================")

