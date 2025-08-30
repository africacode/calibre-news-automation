import os
import time
import subprocess
from email.message import EmailMessage
import smtplib

recipes = {
    'El_Mundo': 'recipes/elmundo.recipe',
}

FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

attachments = []
for name, path in recipes.items():

    # EPUB opcional desde el mismo PDF
    epub_file = f"{name}.epub"
    subprocess.run(['ebook-convert', path, epub_file], check=True)
    attachments.append(epub_file)

    time.sleep(5)

msg = EmailMessage()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = "Tus periódicos del día"

for file in attachments:
    with open(file, 'rb') as f:
        maintype, subtype = ('application', 'pdf') if file.endswith('.pdf') else ('application', 'epub+zip')
        msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=file)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(FROM_EMAIL, APP_PASSWORD)
    smtp.send_message(msg)
