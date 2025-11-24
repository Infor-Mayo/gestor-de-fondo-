"""
Debug del problema de índices en la lista
"""

import os
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def debug_list_indices():
    """Debug de los índices de la lista"""
    print("🔍 DEBUG DE ÍNDICES DE LISTA")
    print("=" * 50)
    
    try:
        from modules.config_manager import ConfigManager
        from modules.wallpaper_engine import WallpaperEngine
        
        # Crear instancias
        config = ConfigManager()
        engine = WallpaperEngine(config)
        
        # Obtener lista completa
        wallpapers = engine.get_wallpaper_list()
        print(f"📋 Total de archivos: {len(wallpapers)}")
        
        if not wallpapers:
            print("❌ No hay archivos en la lista")
            return
        
        # Mostrar todos los archivos con índices
        print(f"\n📄 LISTA COMPLETA:")
        for i, wallpaper in enumerate(wallpapers):
            filename = os.path.basename(wallpaper)
            ext = Path(wallpaper).suffix.lower()
            exists = "✅" if os.path.exists(wallpaper) else "❌"
            print(f"  {i+1:2d}. {exists} {filename} ({ext})")
        
        # Separar como lo hace el código
        images = []
        videos = []
        
        print(f"\n🔍 SEPARACIÓN POR TIPO:")
        for i, wallpaper in enumerate(wallpapers):
            filename = os.path.basename(wallpaper)
            ext = Path(wallpaper).suffix.lower()
            is_video = engine.video_engine.is_video_file(wallpaper)
            
            print(f"  {i+1:2d}. {filename} ({ext}) -> {'🎬 Video' if is_video else '🖼️ Imagen'}")
            
            if is_video:
                videos.append(wallpaper)
            else:
                images.append(wallpaper)
        
        # Verificar totales
        total_original = len(wallpapers)
        total_separated = len(images) + len(videos)
        
        print(f"\n📊 VERIFICACIÓN:")
        print(f"   Original: {total_original} archivos")
        print(f"   Separados: {len(images)} imágenes + {len(videos)} videos = {total_separated}")
        
        if total_original != total_separated:
            print(f"   ⚠️ ERROR: ¡Se perdieron {total_original - total_separated} archivos!")
            
            # Buscar archivos perdidos
            all_separated = images + videos
            print(f"\n🔍 ARCHIVOS PERDIDOS:")
            for wallpaper in wallpapers:
                if wallpaper not in all_separated:
                    filename = os.path.basename(wallpaper)
                    ext = Path(wallpaper).suffix.lower()
                    print(f"   ❌ PERDIDO: {filename} ({ext})")
        else:
            print(f"   ✅ Todos los archivos están correctamente clasificados")
        
        # Mostrar extensiones detectadas
        extensions = {}
        for wallpaper in wallpapers:
            ext = Path(wallpaper).suffix.lower()
            if ext not in extensions:
                extensions[ext] = {'total': 0, 'video': 0, 'image': 0}
            extensions[ext]['total'] += 1
            
            if engine.video_engine.is_video_file(wallpaper):
                extensions[ext]['video'] += 1
            else:
                extensions[ext]['image'] += 1
        
        print(f"\n📈 EXTENSIONES DETECTADAS:")
        for ext, counts in sorted(extensions.items()):
            print(f"   {ext}: {counts['total']} total ({counts['image']} imágenes, {counts['video']} videos)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_list_indices()
