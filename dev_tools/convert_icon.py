"""
Script para convertir el icono de la aplicación a diferentes formatos
"""

from PIL import Image
import os

# Rutas
input_icon = "icono/image-ztBflh0RK44G3gQVq9LGh.webp"
output_dir = "assets"

# Crear directorio si no existe
os.makedirs(output_dir, exist_ok=True)

# Cargar imagen
img = Image.open(input_icon)

# Convertir a PNG
img.save(f"{output_dir}/icon.png", "PNG")
print("✓ Creado: assets/icon.png")

# Crear versión de 64x64 para system tray
img_64 = img.resize((64, 64), Image.Resampling.LANCZOS)
img_64.save(f"{output_dir}/icon_64.png", "PNG")
print("✓ Creado: assets/icon_64.png")

# Crear versión de 32x32
img_32 = img.resize((32, 32), Image.Resampling.LANCZOS)
img_32.save(f"{output_dir}/icon_32.png", "PNG")
print("✓ Creado: assets/icon_32.png")

# Crear versión de 16x16
img_16 = img.resize((16, 16), Image.Resampling.LANCZOS)
img_16.save(f"{output_dir}/icon_16.png", "PNG")
print("✓ Creado: assets/icon_16.png")

# Crear ICO para Windows (múltiples tamaños)
img.save(f"{output_dir}/icon.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
print("✓ Creado: assets/icon.ico")

print("\n✅ Conversión completada!")
