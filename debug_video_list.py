"""
Debug rápido para ver por qué los videos no se detectan en la lista
"""

import os
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def debug_wallpaper_list():
    """Debug de la lista de wallpapers"""
    print("🔍 DEBUG DE LISTA DE WALLPAPERS")
    print("=" * 50)
    
    try:
        from modules.config_manager import ConfigManager
        from modules.wallpaper_engine import WallpaperEngine
        
        # Crear instancias
        config = ConfigManager()
        engine = WallpaperEngine(config)
        
        # Obtener lista
        wallpapers = engine.get_wallpaper_list()
        print(f"📋 Total de archivos en lista: {len(wallpapers)}")
        
        # Analizar cada archivo
        videos = 0
        images = 0
        ext_count = {}
        
        print(f"\n🔍 Analizando archivos:")
        for i, wallpaper in enumerate(wallpapers):
            filename = os.path.basename(wallpaper)
            ext = Path(wallpaper).suffix.lower()
            is_video = engine.video_engine.is_video_file(wallpaper)
            
            # Contar extensiones
            if ext not in ext_count:
                ext_count[ext] = 0
            ext_count[ext] += 1
            
            if is_video:
                videos += 1
                print(f"  {i+1:2d}. 🎬 {filename}")
            else:
                images += 1
                if i < 5:  # Solo mostrar primeras 5 imágenes
                    print(f"  {i+1:2d}. 🖼️ {filename}")
        
        if images > 5:
            print(f"       ... y {images - 5} imágenes más")
        
        print(f"\n📊 RESUMEN:")
        print(f"   🖼️ Imágenes: {images}")
        print(f"   🎬 Videos: {videos}")
        print(f"   📁 Total: {len(wallpapers)}")
        
        print(f"\n📈 POR EXTENSIÓN:")
        for ext, count in sorted(ext_count.items()):
            video_exts = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
            tipo = "🎬" if ext in video_exts else "🖼️"
            print(f"   {tipo} {ext}: {count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_wallpaper_list()
