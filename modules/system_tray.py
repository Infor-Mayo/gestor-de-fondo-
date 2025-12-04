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
            # Resolver base según entorno (EXE vs script)
            if getattr(sys, 'frozen', False):
                base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(__file__)))
                print(f"[TRAY] Ejecutando como EXE. Base: {base_path}")
            else:
                base_path = os.path.dirname(os.path.dirname(__file__))
                print(f"[TRAY] Ejecutando como script. Base: {base_path}")

            # Probar múltiples candidatos (preferir PNG 32x32 para pystray)
            candidates = [
                os.path.join(base_path, 'assets', 'icon_32.png'),
                os.path.join(base_path, 'assets', 'icon.png'),
                os.path.join(base_path, 'assets', 'icon.ico'),
            ]

            for icon_path in candidates:
                print(f"[TRAY] Probando icono: {icon_path}")
                if os.path.exists(icon_path):
                    print(f"[TRAY] ✅ Icono encontrado: {icon_path}")
                    img = PILImage.open(icon_path)
                    try:
                        # Normalizar a 32x32 RGBA para compatibilidad con bandeja
                        img = img.convert('RGBA')
                        if img.size != (32, 32):
                            img = img.resize((32, 32), resample=0)
                    except Exception:
                        pass
                    return img
            print("[TRAY] ⚠️ Ningún icono encontrado en assets")
        except Exception as e:
            print(f"[TRAY] ⚠️ Error cargando icono: {e}")

        # Fallback: icono simple compatible 32x32
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
        # Ejecutar el icono en modo detached para evitar bloqueo y mejorar aparición
        try:
            self.icon.run_detached()
        except Exception:
            # Fallback al modo normal
            try:
                self.icon.visible = True
            except Exception:
                pass
            self.icon.run()
        # Forzar visibilidad después de iniciar
        try:
            self.icon.visible = True
        except Exception:
            pass

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

    def update_countdown(self, minutes: int, seconds: int):
        """
        Actualiza el título del icono con el tiempo restante.
        Llama mediante root.after para evitar problemas de threading.
        """
        if not self.icon:
            return

        try:
            if minutes > 0:
                text = f"{self.base_title} — Próximo cambio: {minutes}m {seconds}s"
            else:
                text = f"{self.base_title} — Próximo cambio: {seconds}s"

            def do_update():
                try:
                    self.icon.title = text
                except Exception:
                    pass

            try:
                self.root.after(0, do_update)
            except Exception:
                # Si root no está disponible, intentamos directamente
                do_update()
        except Exception:
            # Evitar que un fallo en bandeja detenga el hilo del motor
            pass
