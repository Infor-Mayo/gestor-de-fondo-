"""
Test simple de video animado como fondo de pantalla
"""

import os
import sys
from pathlib import Path

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def test_simple_video():
    """Prueba simple de video"""
    print("🎬 PRUEBA SIMPLE DE VIDEO ANIMADO")
    print("=" * 40)
    
    try:
        from modules.config_manager import ConfigManager
        from modules.video_wallpaper import VideoWallpaperEngine
        
        # Crear instancias
        config = ConfigManager()
        video_engine = VideoWallpaperEngine()
        
        # Obtener primer video de la lista
        wallpapers = config.get("wallpapers", [])
        video_file = None
        
        for wallpaper in wallpapers:
            if video_engine.is_video_file(wallpaper):
                video_file = wallpaper
                break
        
        if not video_file:
            print("❌ No hay videos en la configuración")
            return False
        
        print(f"🎯 Video seleccionado: {os.path.basename(video_file)}")
        
        # Probar establecer como fondo
        success = video_engine.set_video_wallpaper(video_file)
        
        if success:
            print("✅ Video establecido como fondo")
            print("💡 Deberías ver una ventana de video en pantalla completa")
            print("⏰ El video se reproducirá en bucle")
            
            # Esperar un poco para que se vea
            import time
            print("⏳ Esperando 10 segundos para que veas el video...")
            time.sleep(10)
            
            # Detener video
            print("🛑 Deteniendo video...")
            video_engine.stop_video_wallpaper()
            
            return True
        else:
            print("❌ No se pudo establecer el video")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_video()
    
    if success:
        print("\n🎉 ¡Prueba exitosa!")
        print("💡 Si viste el video reproduciéndose, la funcionalidad está trabajando.")
    else:
        print("\n❌ Prueba falló.")
        print("💡 Puede que necesites instalar dependencias adicionales:")
        print("   pip install opencv-python pillow")
