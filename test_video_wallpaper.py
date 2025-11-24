"""
Test rápido para probar la funcionalidad de video como fondo de pantalla
"""

import os
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def test_video_wallpaper():
    """Prueba establecer un video como fondo de pantalla"""
    print("🎬 PRUEBA DE VIDEO COMO FONDO DE PANTALLA")
    print("=" * 50)
    
    try:
        from modules.config_manager import ConfigManager
        from modules.video_wallpaper import VideoWallpaperEngine
        
        # Crear instancias
        config = ConfigManager()
        video_engine = VideoWallpaperEngine()
        
        # Obtener lista de wallpapers
        wallpapers = config.get("wallpapers", [])
        print(f"📋 Total de archivos en configuración: {len(wallpapers)}")
        
        # Buscar el primer video
        video_file = None
        for wallpaper in wallpapers:
            if video_engine.is_video_file(wallpaper):
                video_file = wallpaper
                break
        
        if not video_file:
            print("❌ No se encontraron videos en la configuración")
            return False
        
        print(f"🎯 Probando video: {os.path.basename(video_file)}")
        
        # Verificar que el archivo existe
        if not os.path.exists(video_file):
            print(f"❌ El archivo no existe: {video_file}")
            return False
        
        print(f"✅ Archivo existe: {video_file}")
        
        # Intentar establecer como fondo
        print(f"🎬 Estableciendo video como fondo de pantalla...")
        success = video_engine.set_video_wallpaper(video_file)
        
        if success:
            print(f"🎉 ¡Video establecido como fondo exitosamente!")
            print(f"💡 Deberías ver el primer frame del video como fondo de pantalla")
            return True
        else:
            print(f"❌ No se pudo establecer el video como fondo")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_video_wallpaper()
    
    if success:
        print(f"\n✅ Prueba exitosa!")
        print(f"💡 Si ves una imagen del video como fondo, la funcionalidad está trabajando.")
        print(f"📝 Nota: Por limitaciones técnicas, se muestra el primer frame del video")
        print(f"    en lugar de reproducción continua.")
    else:
        print(f"\n❌ Prueba falló. Revisa los logs para más detalles.")
