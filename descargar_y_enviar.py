import os
import time
import subprocess
from email.message import EmailMessage
import smtplib
from pathlib import Path
from datetime import datetime

# 📚 Recetas disponibles
recipes = {
    'El_Mundo': 'recipes/elmundo.recipe',
}

# 📩 Configuración de correo desde variables de entorno
FROM_EMAIL = os.getenv('FROM_EMAIL')
TO_EMAIL = os.getenv('TO_EMAIL')
APP_PASSWORD = os.getenv('APP_PASSWORD')

# 📂 Carpeta de salida
OUTPUT_DIR = Path("/app/output")
OUTPUT_DIR.mkdir(exist_ok=True, parents=True)

today = datetime.now().strftime("%Y-%m-%d")
attachments = []

for name, path in recipes.items():
    recipe_path = Path(path)

    # ✅ Verificar que la receta existe
    if not recipe_path.exists():
        raise FileNotFoundError(f"❌ No se encontró la receta en {recipe_path}. "
                                "¿Seguro que está copiada dentro del contenedor?")

    # 📖 Nombre de salida con fecha
    epub_file = OUTPUT_DIR / f"{name}_{today}.epub"

    print(f"➡️ Generando {epub_file} con {recipe_path}...")
    subprocess.run([
        "ebook-convert", str(recipe_path), str(epub_file)
    ], check=True)

    attachments.append(epub_file)
    time.sleep(5)

# ✉️ Preparar correo
msg = EmailMessage()
msg['From'] = FROM_EMAIL
msg['To'] = TO_EMAIL
msg['Subject'] = f"Tus periódicos del día - {today}"

for file in attachments:
    with open(file, 'rb') as f:
        maintype, subtype = ('application', 'epub+zip')
        msg.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=file.name)

# 📤 Enviar correo
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(FROM_EMAIL, APP_PASSWORD)
    smtp.send_message(msg)

print("✅ Correo enviado con éxito.")

