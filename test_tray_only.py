"""
Test simple del system tray
"""

import sys
import os

# Agregar módulos al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

try:
    from modules.system_tray import SystemTrayManager
    
    def dummy_callback():
        print("Callback ejecutado")
    
    print("🔍 Probando SystemTrayManager...")
    
    tray = SystemTrayManager(
        on_show=dummy_callback,
        on_change_now=dummy_callback,
        on_quit=dummy_callback
    )
    
    print("✅ SystemTrayManager creado")
    
    # Probar crear icono
    image = tray.create_icon_image()
    print(f"✅ Imagen creada: {image.size}")
    
    # Configurar tray
    tray.setup()
    print("✅ Tray configurado")
    
    print("💡 Busca el icono en la bandeja del sistema")
    print("   Presiona Ctrl+C para salir")
    
    # Mantener vivo
    tray.run()
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
