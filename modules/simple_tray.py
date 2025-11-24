"""
System Tray simplificado que funciona mejor en EXE
"""

import threading
import os
import sys
from typing import Callable

try:
    import pystray
    from PIL import Image as PILImage
    PYSTRAY_AVAILABLE = True
except ImportError:
    PYSTRAY_AVAILABLE = False

class SimpleTrayManager:
    """Gestor simplificado de bandeja del sistema"""
    
    def __init__(self, on_show: Callable, on_quit: Callable):
        self.on_show = on_show
        self.on_quit = on_quit
        self.icon = None
        self.running = False
        self.ready = False  # Flag para indicar que el icono está listo
        
    def create_simple_icon(self):
        """Crea un icono simple"""
        try:
            # Intentar cargar icono desde assets
            if getattr(sys, 'frozen', False):
                # EXE
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icon_32.png')
            else:
                # Script
                base_dir = os.path.dirname(os.path.dirname(__file__))
                icon_path = os.path.join(base_dir, 'assets', 'icon_32.png')
            
            if os.path.exists(icon_path):
                return PILImage.open(icon_path)
        except:
            pass
        
        # Fallback: crear icono simple
        return PILImage.new('RGB', (32, 32), color='#2196F3')
    
    def setup(self):
        """Configura el icono de bandeja"""
        if not PYSTRAY_AVAILABLE:
            print("[ADVERTENCIA] pystray no disponible")
            return False
        
        try:
            image = self.create_simple_icon()
            
            menu = pystray.Menu(
                pystray.MenuItem("Mostrar Ventana", self.on_show, default=True),
                pystray.MenuItem("Cambiar Fondo Ahora", self.change_wallpaper),
                pystray.Menu.SEPARATOR,
                pystray.MenuItem("Salir", self.on_quit)
            )
            
            # Crear el icono - NO usar visible=True aquí, lo haremos después
            self.icon = pystray.Icon(
                "CambiadorFondo",
                image,
                "Cambiador de Fondo de Pantalla - Clic derecho para opciones",
                menu
            )
            
            # Ejecutar en hilo separado (no daemon para que no se cierre)
            self.thread = threading.Thread(target=self._run_icon, daemon=False, name="TrayIconThread")
            self.thread.start()
            
            # Esperar un momento para que el hilo inicie
            import time
            max_wait = 1.5
            waited = 0.0
            while not self.running and waited < max_wait:
                time.sleep(0.1)
                waited += 0.1
            
            if self.running:
                print("[DEBUG] Hilo del icono está corriendo")
                # Asegurar visibilidad después de iniciar
                try:
                    if self.icon:
                        # Forzar visibilidad múltiples veces
                        self.icon.visible = True
                        print("[DEBUG] Icono marcado como visible (intento 1)")
                        # Intentar de nuevo después de un momento
                        import time
                        time.sleep(0.2)
                        self.icon.visible = True
                        print("[DEBUG] Icono marcado como visible (intento 2)")
                except Exception as e:
                    print(f"[ADVERTENCIA] Error estableciendo visibilidad: {e}")
            else:
                print("[ADVERTENCIA] Hilo del icono no inició en el tiempo esperado")
            
            # Marcar como listo
            self.ready = True
            
            # Intentar mostrar notificación después de un delay
            def show_notification():
                try:
                    if self.icon and self.running:
                        self.icon.notify(
                            "Aplicación en segundo plano",
                            "El icono está en el área de notificaciones.\nClic derecho para opciones."
                        )
                except:
                    pass
            
            # Programar notificación para después
            threading.Timer(1.5, show_notification).start()
            
            print("[OK] Icono de bandeja configurado - hilo iniciado")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error configurando bandeja: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _run_icon(self):
        """Ejecuta el icono en hilo separado"""
        try:
            print("[DEBUG] Iniciando icono en hilo separado...")
            
            if not self.icon:
                print("[ERROR] No hay icono para ejecutar")
                return
            
            # Marcar como corriendo ANTES de ejecutar
            self.running = True
            print("[DEBUG] Hilo marcado como corriendo")
            
            # Asegurar que el icono sea visible ANTES de ejecutar run()
            try:
                self.icon.visible = True
                print("[DEBUG] Visibilidad del icono establecida antes de run()")
                # Esperar un momento y verificar
                import time
                time.sleep(0.1)
                if hasattr(self.icon, 'visible'):
                    print(f"[DEBUG] Estado de visibilidad antes de run(): {self.icon.visible}")
            except Exception as e:
                print(f"[ADVERTENCIA] No se pudo establecer visibilidad antes de run(): {e}")
            
            # Ejecutar el icono (esto bloquea hasta que se detenga)
            print("[DEBUG] Ejecutando icon.run()...")
            self.icon.run()
            print("[DEBUG] icon.run() terminó")
        except Exception as e:
            print(f"[ERROR] Error ejecutando icono: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.running = False
            print("[DEBUG] Hilo del icono terminado")
    
    def change_wallpaper(self, icon=None, item=None):
        """Callback para cambiar wallpaper"""
        # Este método puede ser sobrescrito
        pass
    
    def set_visible(self, visible=True):
        """Fuerza la visibilidad del icono"""
        if self.icon:
            try:
                self.icon.visible = visible
                # Forzar actualización
                if hasattr(self.icon, 'update_menu'):
                    self.icon.update_menu()
            except Exception as e:
                print(f"[ADVERTENCIA] Error estableciendo visibilidad: {e}")
    
    def is_ready(self):
        """Verifica si el icono está listo"""
        return self.ready and self.icon is not None
    
    def notify(self, title, message):
        """Muestra una notificación"""
        if self.icon:
            try:
                self.icon.notify(title, message)
            except:
                pass
    
    def stop(self):
        """Detiene el icono"""
        if self.icon and self.running:
            try:
                self.icon.stop()
                self.running = False
            except:
                pass
