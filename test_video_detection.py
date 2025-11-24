"""
Prueba simple para verificar detección de videos
"""

import os
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def test_video_detection():
    """Prueba la detección de videos"""
    print("🧪 PRUEBA DE DETECCIÓN DE VIDEOS")
    print("=" * 40)
    
    try:
        from modules.video_wallpaper import VideoWallpaperEngine
        
        video_engine = VideoWallpaperEngine()
        
        # Archivos de prueba
        test_files = [
            "video.mp4",
            "movie.avi", 
            "clip.mov",
            "animation.wmv",
            "film.mkv",
            "image.jpg",
            "photo.png"
        ]
        
        print("Probando detección de archivos:")
        for file in test_files:
            is_video = video_engine.is_video_file(file)
            ext = Path(file).suffix.lower()
            status = "✅ Video" if is_video else "❌ No es video"
            print(f"  {file} ({ext}) -> {status}")
        
        print(f"\n🔍 Extensiones de video soportadas:")
        video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        for ext in sorted(video_extensions):
            print(f"  {ext}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_config_manager():
    """Prueba el config manager"""
    print(f"\n📋 PRUEBA DE CONFIG MANAGER")
    print("=" * 40)
    
    try:
        from modules.config_manager import ConfigManager
        
        config = ConfigManager()
        
        # Obtener lista actual
        wallpapers = config.get("wallpapers", [])
        print(f"Fondos actuales en config: {len(wallpapers)}")
        
        for i, wallpaper in enumerate(wallpapers[:5], 1):
            filename = os.path.basename(wallpaper)
            ext = Path(wallpaper).suffix.lower()
            print(f"  {i}. {filename} ({ext})")
        
        if len(wallpapers) > 5:
            print(f"  ... y {len(wallpapers) - 5} más")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success1 = test_video_detection()
    success2 = test_config_manager()
    
    if success1 and success2:
        print(f"\n✅ Todas las pruebas pasaron")
    else:
        print(f"\n❌ Algunas pruebas fallaron")
