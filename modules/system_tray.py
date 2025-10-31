"""
Módulo de bandeja del sistema
Maneja el icono y menú en la bandeja del sistema
"""

import threading
import pystray
from PIL import Image as PILImage
from typing import Callable, Optional


class SystemTrayManager:
    """Gestiona el icono en la bandeja del sistema"""
    
    def __init__(self, 
                 on_show: Callable,
                 on_change_now: Callable,
                 on_quit: Callable):
        """
        Inicializa el gestor de bandeja del sistema
        
        Args:
            on_show: Callback para mostrar la ventana
            on_change_now: Callback para cambiar el fondo ahora
            on_quit: Callback para salir de la aplicación
        """
        self.on_show = on_show
        self.on_change_now = on_change_now
        self.on_quit = on_quit
        self.icon = None
        self.base_title = "Cambiador de Fondo"
    
    def create_icon_image(self) -> PILImage.Image:
        """
        Crea una imagen simple para el icono
        
        Returns:
            Imagen PIL para el icono
        """
        # Intentar cargar el icono de la aplicación
        try:
            import os
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icon_64.png")
            if os.path.exists(icon_path):
                return PILImage.open(icon_path)
        except:
            pass
        
        # Fallback: crear una imagen simple de 64x64 azul
        image = PILImage.new('RGB', (64, 64), color='#2196F3')
        return image
    
    def setup(self) -> None:
        """Configura e inicia el icono en la bandeja"""
        image = self.create_icon_image()
        
        menu = pystray.Menu(
            pystray.MenuItem("Abrir", self.on_show, default=True),
            pystray.MenuItem("Cambiar Fondo Ahora", self.on_change_now),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Salir", self.on_quit)
        )
        
        self.icon = pystray.Icon(
            "WallpaperChanger",
            image,
            self.base_title,
            menu
        )
        
        # Iniciar el icono en un thread separado
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def update_title(self, title: str) -> None:
        """
        Actualiza el título del icono (tooltip)
        
        Args:
            title: Nuevo título a mostrar
        """
        if self.icon:
            self.icon.title = title
    
    def update_countdown(self, minutes: int, seconds: int) -> None:
        """
        Actualiza el tooltip con el contador regresivo
        
        Args:
            minutes: Minutos restantes
            seconds: Segundos restantes
        """
        if minutes > 0:
            countdown_text = f"{self.base_title}\n⏰ Próximo cambio: {minutes}m {seconds}s"
        else:
            countdown_text = f"{self.base_title}\n⏰ Próximo cambio: {seconds}s"
        self.update_title(countdown_text)
    
    def reset_title(self) -> None:
        """Resetea el título al valor base"""
        self.update_title(self.base_title)
    
    def stop(self) -> None:
        """Detiene el icono de la bandeja"""
        if self.icon:
            self.icon.stop()
    
    def notify(self, title: str, message: str) -> None:
        """
        Muestra una notificación
        
        Args:
            title: Título de la notificación
            message: Mensaje de la notificación
        """
        if self.icon:
            self.icon.notify(title, message)
