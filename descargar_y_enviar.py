import os
import time
import subprocess
from email.message import EmailMessage
import smtplib

recipes = {
    'El_Mundo': 'recipes/elmundo.recipe',
    'Expansion': 'recipes/expansion_spanish.recipe',
    'Wall_Street_Journal': 'recipes/wsj_news.recipe',
    'El_Pais': 'recipes/elpais.recipe',
    'Financial_Times': 'recipes/financial_times.recipe'
}

FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

epubs = []
for name, path in recipes.items():
    epub = f"{name}.epub"
    subprocess.run(['ebook-convert', path, epub], check=True)
    epubs.append(epub)
    time.sleep(5)

msg = EmailMessage()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = "Tus periódicos del día"

for epub in epubs:
    with open(epub, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='epub+zip', filename=epub)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(FROM_EMAIL, APP_PASSWORD)
    smtp.send_message(msg)
