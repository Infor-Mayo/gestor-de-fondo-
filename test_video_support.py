"""
Script de prueba para verificar el soporte de videos
Prueba las funcionalidades básicas del nuevo módulo de videos
"""

import os
import sys
import time
from pathlib import Path

# Agregar el directorio modules al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.video_wallpaper import VideoWallpaperEngine
from modules.wallpaper_engine import WallpaperEngine
from modules.config_manager import ConfigManager

def test_video_detection():
    """Prueba la detección de archivos de video"""
    print("🎬 Probando detección de videos...")
    
    video_engine = VideoWallpaperEngine()
    
    # Archivos de prueba
    test_files = [
        "video.mp4",
        "movie.avi", 
        "clip.mov",
        "animation.wmv",
        "film.mkv",
        "image.jpg",
        "photo.png",
        "document.txt"
    ]
    
    for file in test_files:
        is_video = video_engine.is_video_file(file)
        status = "✓ Video" if is_video else "✗ No es video"
        print(f"  {file}: {status}")
    
    print()

def test_wallpaper_engine_integration():
    """Prueba la integración con WallpaperEngine"""
    print("🔧 Probando integración con WallpaperEngine...")
    
    config_manager = ConfigManager()
    wallpaper_engine = WallpaperEngine(config_manager)
    
    # Verificar que el motor de video está inicializado
    if hasattr(wallpaper_engine, 'video_engine'):
        print("  ✓ Motor de video inicializado correctamente")
    else:
        print("  ✗ Error: Motor de video no encontrado")
        return False
    
    # Verificar método get_media_from_folder
    if hasattr(wallpaper_engine, 'get_media_from_folder'):
        print("  ✓ Método get_media_from_folder disponible")
    else:
        print("  ✗ Error: Método get_media_from_folder no encontrado")
        return False
    
    print()
    return True

def test_folder_scanning():
    """Prueba el escaneo de carpetas para videos e imágenes"""
    print("📁 Probando escaneo de carpetas...")
    
    config_manager = ConfigManager()
    wallpaper_engine = WallpaperEngine(config_manager)
    
    # Crear carpeta de prueba temporal
    test_folder = os.path.join(os.path.dirname(__file__), "test_media")
    
    if not os.path.exists(test_folder):
        print(f"  📂 Carpeta de prueba no existe: {test_folder}")
        print("  💡 Crea una carpeta 'test_media' con algunos videos e imágenes para probar")
        return
    
    # Escanear archivos
    media_files = wallpaper_engine.get_media_from_folder(test_folder)
    image_files = wallpaper_engine.get_images_from_folder(test_folder)
    
    print(f"  📊 Archivos encontrados:")
    print(f"    Total de medios: {len(media_files)}")
    print(f"    Solo imágenes: {len(image_files)}")
    print(f"    Videos: {len(media_files) - len(image_files)}")
    
    if media_files:
        print(f"  📋 Lista de archivos:")
        for i, file in enumerate(media_files[:5], 1):  # Mostrar solo los primeros 5
            file_type = "🎬" if wallpaper_engine.video_engine.is_video_file(file) else "🖼️"
            print(f"    {i}. {file_type} {os.path.basename(file)}")
        
        if len(media_files) > 5:
            print(f"    ... y {len(media_files) - 5} archivo(s) más")
    
    print()

def test_dependencies():
    """Verifica que las dependencias necesarias estén instaladas"""
    print("📦 Verificando dependencias...")
    
    dependencies = [
        ("opencv-python", "cv2"),
        ("numpy", "numpy"),
        ("Pillow", "PIL"),
        ("customtkinter", "customtkinter")
    ]
    
    all_ok = True
    
    for dep_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"  ✓ {dep_name}")
        except ImportError:
            print(f"  ✗ {dep_name} - NO INSTALADO")
            all_ok = False
    
    if not all_ok:
        print("\n  ⚠️  Instala las dependencias faltantes con:")
        print("     pip install -r requirements.txt")
    
    print()
    return all_ok

def main():
    """Función principal de pruebas"""
    print("🧪 PRUEBAS DE SOPORTE DE VIDEOS")
    print("=" * 50)
    print()
    
    # Ejecutar todas las pruebas
    test_dependencies()
    test_video_detection()
    
    if test_wallpaper_engine_integration():
        test_folder_scanning()
    
    print("🎉 Pruebas completadas!")
    print("\n💡 Para probar completamente:")
    print("   1. Crea una carpeta 'test_media' con videos e imágenes")
    print("   2. Ejecuta la aplicación principal: python main.py")
    print("   3. Selecciona la carpeta y prueba el cambio de fondos")

if __name__ == "__main__":
    main()
