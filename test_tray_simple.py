"""
Script de prueba simple para verificar que el system tray funciona
"""
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from modules.simple_tray import SimpleTrayManager
    import time
    
    def on_show():
        print("Mostrar ventana llamado")
    
    def on_quit():
        print("Salir llamado")
        sys.exit(0)
    
    print("Creando icono de bandeja...")
    tray = SimpleTrayManager(on_show=on_show, on_quit=on_quit)
    
    if tray.setup():
        print("Icono configurado correctamente")
        print("El icono debería aparecer en el área de notificaciones")
        print("Presiona Ctrl+C para salir o usa el menú del icono")
        
        # Mantener el script corriendo
        try:
            while True:
                time.sleep(1)
                if tray.icon and hasattr(tray.icon, 'visible'):
                    print(f"Estado del icono - Visible: {tray.icon.visible}, Running: {tray.running}")
        except KeyboardInterrupt:
            print("\nCerrando...")
            tray.stop()
    else:
        print("Error configurando el icono")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    input("Presiona Enter para continuar...")

