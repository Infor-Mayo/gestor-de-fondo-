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
    from PIL import ImageDraw
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
            import sys
            # Determinar base
            if getattr(sys, 'frozen', False):
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(__file__)))
                print(f"[TRAY-SIMPLE] Ejecutando como EXE. Base: {base_path}")
            else:
                base_path = os.path.dirname(os.path.dirname(__file__))
                print(f"[TRAY-SIMPLE] Ejecutando como script. Base: {base_path}")

            candidates = [
                os.path.join(base_path, 'assets', 'icon_32.png'),
                os.path.join(base_path, 'assets', 'icon.png'),
                os.path.join(base_path, 'assets', 'icon.ico'),
            ]
            for icon_path in candidates:
                print(f"[TRAY-SIMPLE] Probando icono: {icon_path}")
                if os.path.exists(icon_path):
                    img = PILImage.open(icon_path)
                    try:
                        img = img.convert('RGBA')
                        if img.size != (32, 32):
                            img = img.resize((32, 32), resample=0)
                    except Exception:
                        pass
                    return img
        except Exception as e:
            print(f"[TRAY-SIMPLE] Error cargando icono: {e}")

        # Fallback: crear icono simple
        img = PILImage.new("RGB", (32, 32), "#2196F3")
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 24, 24), fill="white")
        return img
    
    def setup(self):
        """Configura el icono de bandeja"""
        if not PYSTRAY_AVAILABLE:
            print("[ADVERTENCIA] pystray no disponible")
            return False
        
        try:
            image = self.create_simple_icon()
            
            # Acciones adicionales
            def abrir_config(icon=None, item=None):
                try:
                    import sys
                    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(__file__))) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.dirname(__file__))
                    cfg = os.path.join(base_path, 'config.json')
                    if os.path.exists(cfg):
                        os.startfile(cfg)
                    else:
                        os.startfile(base_path)
                except Exception:
                    pass

            def habilitar_inicio(icon=None, item=None):
                try:
                    from .startup_manager import StartupManager
                    ok, msg = StartupManager.enable()
                    try:
                        self.notify("Inicio automático", msg)
                    except Exception:
                        pass
                except Exception:
                    pass

            def deshabilitar_inicio(icon=None, item=None):
                try:
                    from .startup_manager import StartupManager
                    ok, msg = StartupManager.disable()
                    try:
                        self.notify("Inicio automático", msg)
                    except Exception:
                        pass
                except Exception:
                    pass

            menu = pystray.Menu(
                pystray.MenuItem("Mostrar Ventana", self.on_show, default=True),
                pystray.MenuItem("Cambiar Fondo Ahora", self.change_wallpaper),
                pystray.MenuItem("Abrir Configuración", abrir_config),
                pystray.MenuItem("Habilitar inicio automático", habilitar_inicio),
                pystray.MenuItem("Deshabilitar inicio automático", deshabilitar_inicio),
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
        """Detiene el icono y espera que el hilo termine"""
        try:
            if self.icon:
                try:
                    self.icon.stop()
                except Exception:
                    pass
            # Marcar estado
            self.running = False
            # Esperar a que el hilo de icono termine si existe
            if hasattr(self, 'thread') and self.thread:
                try:
                    if self.thread.is_alive():
                        self.thread.join(timeout=2)
                except Exception:
                    pass
            # Liberar referencia al icono
            self.icon = None
        except Exception:
            pass
