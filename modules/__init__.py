"""
Módulos del Cambiador de Fondo de Pantalla
Versión 2.1 - Ahora con soporte para videos
"""

__version__ = "2.1.0"
__author__ = "Cambiador de Fondo Team"

# Función helper para prints seguros sin emojis
def safe_print(*args, **kwargs):
    """Función de print que maneja errores de codificación de forma segura"""
    try:
        print(*args, **kwargs)
    except UnicodeEncodeError:
        # Si hay error de codificación, reemplazar emojis comunes
        safe_args = []
        for arg in args:
            if isinstance(arg, str):
                # Reemplazar emojis comunes con texto
                arg = arg.replace('✅', '[OK]').replace('❌', '[ERROR]')
                arg = arg.replace('⚠️', '[ADVERTENCIA]').replace('📱', '[INFO]')
                arg = arg.replace('🚀', '[INFO]').replace('⚙️', '[CONFIG]')
                arg = arg.replace('🎬', '[VIDEO]').replace('🖼️', '[IMAGEN]')
                arg = arg.replace('📋', '[LISTA]').replace('💡', '[TIP]')
                arg = arg.replace('🗑️', '[ELIMINAR]').replace('🖱️', '[MOUSE]')
                arg = arg.replace('👋', '[INFO]').replace('🎯', '[INFO]')
            safe_args.append(arg)
        try:
            print(*safe_args, **kwargs)
        except:
            # Si aún falla, usar encoding con reemplazo de errores
            import sys
            for arg in safe_args:
                sys.stdout.buffer.write(str(arg).encode('utf-8', errors='replace') + b'\n')

# Importaciones principales
from .wallpaper_engine import WallpaperEngine
from .video_wallpaper import VideoWallpaperEngine
from .config_manager import ConfigManager
from .gui import WallpaperChangerGUI
from .startup_manager import StartupManager

# Importar system tray de forma opcional
try:
    from .system_tray import SystemTrayManager
    _system_tray_available = True
except ImportError:
    SystemTrayManager = None
    _system_tray_available = False

__all__ = [
    'WallpaperEngine',
    'VideoWallpaperEngine', 
    'ConfigManager',
    'WallpaperChangerGUI',
    'StartupManager'
]

# Solo agregar SystemTrayManager si está disponible
if _system_tray_available:
    __all__.append('SystemTrayManager')
