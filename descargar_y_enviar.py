import os
import subprocess
from datetime import datetime

# Diccionario de recetas disponibles
recipes = {
    "elmundo": "recipes/elmundo.recipe"
}

# Carpeta de salida
output_dir = "/app/output"

def descargar_noticias():
    for nombre, ruta in recipes.items():
        salida = os.path.join(output_dir, f"{nombre}_{datetime.now().strftime('%Y-%m-%d')}.epub")
        print(f"📥 Descargando {nombre} con receta {ruta}...")
        subprocess.run([
            "ebook-convert", ruta, salida
        ], check=True)
        print(f"✅ Guardado en {salida}")

if __name__ == "__main__":
    descargar_noticias()
