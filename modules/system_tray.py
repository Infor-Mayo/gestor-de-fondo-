import threading
import pystray
from PIL import Image as PILImage
from PIL import ImageDraw
import os


class SystemTrayManager:
    def __init__(self, root, on_show, on_change_now, on_quit):
        self.root = root
        self.on_show = on_show
        self.on_change_now = on_change_now
        self.on_quit = on_quit
        self.icon = None
        self.base_title = "Cambiador de Fondo"

    def create_icon_image(self):
        try:
            import sys
            # Detectar si estamos en EXE o script
            if getattr(sys, 'frozen', False):
                # Ejecutándose como EXE - usar sys._MEIPASS
                icon_path = os.path.join(sys._MEIPASS, 'assets', 'icon_32.png')
                print(f"[TRAY] Buscando icono en EXE: {icon_path}")
            else:
                # Ejecutándose como script - subir dos niveles desde modules/ a la raíz
                base_dir = os.path.dirname(os.path.dirname(__file__))
                icon_path = os.path.join(base_dir, 'assets', 'icon_32.png')
                print(f"[TRAY] Buscando icono en script: {icon_path}")

            if os.path.exists(icon_path):
                print(f"[TRAY] ✅ Icono encontrado: {icon_path}")
                return PILImage.open(icon_path)
            else:
                print(f"[TRAY] ⚠️ Icono no encontrado: {icon_path}")
        except Exception as e:
            print(f"[TRAY] ⚠️ Error cargando icono: {e}")

        # fallback: icono simple compatible 32x32
        print("[TRAY] Usando icono fallback generado")
        img = PILImage.new("RGB", (32, 32), "#2196F3")
        draw = ImageDraw.Draw(img)
        draw.ellipse((8, 8, 24, 24), fill="white")
        return img

    def crear_icono(self):
        image = self.create_icon_image()

        def mostrar(icon, item):
            self.root.after(0, self.on_show)

        def cambiar(icon, item):
            self.root.after(0, self.on_change_now)

        def salir(icon, item):
            self.root.after(0, self.on_quit)

        menu = pystray.Menu(
            pystray.MenuItem("Abrir", mostrar, default=True),
            pystray.MenuItem("Cambiar Fondo Ahora", cambiar),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Salir", salir)
        )

        self.icon = pystray.Icon(
            "CambiadorFondo", image, self.base_title, menu)
        self.icon.run()

    def setup(self):
        threading.Thread(target=self.crear_icono, daemon=True).start()

    def stop(self):
        if self.icon:
            self.icon.stop()

    def notify(self, title, msg):
        if self.icon:
            self.icon.notify(title, msg)

    def update_title(self, text):
        if self.icon:
            self.icon.title = text
