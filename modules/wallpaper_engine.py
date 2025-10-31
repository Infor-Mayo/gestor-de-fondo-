"""
Módulo del motor de cambio de fondos
Maneja la lógica de cambio de fondos de pantalla
"""

import os
import ctypes
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional, Callable

from .config_manager import ConfigManager


class WallpaperEngine:
    """Motor para cambiar fondos de pantalla"""
    
    def __init__(self, config_manager: ConfigManager):
        """
        Inicializa el motor de fondos
        
        Args:
            config_manager: Instancia del gestor de configuración
        """
        self.config_manager = config_manager
        self.running = False
        self.thread = None
        self.countdown_callback = None
    
    def set_wallpaper(self, image_path: str) -> bool:
        """
        Cambia el fondo de pantalla en Windows
        
        Args:
            image_path: Ruta a la imagen
            
        Returns:
            True si se cambió correctamente, False en caso contrario
        """
        try:
            abs_path = os.path.abspath(image_path)
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                abs_path, 
                3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            return True
        except Exception as e:
            print(f"Error cambiando fondo: {e}")
            return False
    
    def get_images_from_folder(self, folder_path: Optional[str] = None) -> List[str]:
        """
        Obtiene todas las imágenes de una carpeta
        
        Args:
            folder_path: Ruta de la carpeta. Si es None, usa la configurada
            
        Returns:
            Lista de rutas de imágenes
        """
        if folder_path is None:
            folder_path = self.config_manager.get("wallpaper_folder")
        
        if not folder_path or not os.path.exists(folder_path):
            return []
        
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        images = []
        
        try:
            for file in os.listdir(folder_path):
                if Path(file).suffix.lower() in valid_extensions:
                    full_path = os.path.join(folder_path, file)
                    images.append(full_path)
        except Exception as e:
            print(f"Error leyendo carpeta: {e}")
        
        return sorted(images)
    
    def get_wallpaper_list(self) -> List[str]:
        """
        Obtiene la lista de fondos según la configuración
        
        Returns:
            Lista de rutas de fondos
        """
        if self.config_manager.get("use_folder", False):
            return self.get_images_from_folder()
        else:
            return self.config_manager.get("wallpapers", [])
    
    def get_next_wallpaper_time_mode(self) -> Optional[str]:
        """
        Obtiene el siguiente fondo en modo tiempo
        
        Returns:
            Ruta del siguiente fondo o None si no hay fondos
        """
        wallpapers = self.get_wallpaper_list()
        
        if not wallpapers:
            return None
        
        current_index = self.config_manager.get("current_index", 0)
        wallpaper = wallpapers[current_index]
        
        # Actualizar índice
        new_index = (current_index + 1) % len(wallpapers)
        self.config_manager.set("current_index", new_index)
        self.config_manager.save_config()
        
        return wallpaper
    
    def get_wallpaper_for_today(self) -> Optional[str]:
        """
        Obtiene el fondo para el día actual
        
        Returns:
            Ruta del fondo del día o None
        """
        weekday = str(datetime.now().weekday())
        weekday_wallpapers = self.config_manager.get("weekday_wallpapers", {})
        return weekday_wallpapers.get(weekday)
    
    def should_change_wallpaper(self) -> bool:
        """
        Determina si debe cambiar el fondo
        
        Returns:
            True si debe cambiar, False en caso contrario
        """
        mode = self.config_manager.get("mode", "time")
        
        if mode == "time":
            last_change = self.config_manager.get("last_change")
            if not last_change:
                return True
            
            last_change_dt = datetime.fromisoformat(last_change)
            interval = timedelta(minutes=self.config_manager.get("interval_minutes", 30))
            return datetime.now() - last_change_dt >= interval
        
        elif mode == "weekday":
            last_change = self.config_manager.get("last_change")
            if not last_change:
                return True
            
            last_change_dt = datetime.fromisoformat(last_change)
            return last_change_dt.date() != datetime.now().date()
        
        return False
    
    def change_wallpaper(self) -> bool:
        """
        Cambia el fondo de pantalla según la configuración
        
        Returns:
            True si se cambió correctamente, False en caso contrario
        """
        mode = self.config_manager.get("mode", "time")
        
        if mode == "time":
            wallpaper = self.get_next_wallpaper_time_mode()
        else:
            wallpaper = self.get_wallpaper_for_today()
        
        if wallpaper and os.path.exists(wallpaper):
            if self.set_wallpaper(wallpaper):
                self.config_manager.set("last_change", datetime.now().isoformat())
                self.config_manager.save_config()
                return True
        return False
    
    def get_time_until_next_change(self) -> Optional[int]:
        """
        Obtiene los segundos hasta el próximo cambio
        
        Returns:
            Segundos hasta el próximo cambio o None si no aplica
        """
        mode = self.config_manager.get("mode", "time")
        
        if mode != "time":
            return None
        
        last_change = self.config_manager.get("last_change")
        if not last_change:
            return 0
        
        try:
            last_change_dt = datetime.fromisoformat(last_change)
            interval = timedelta(minutes=self.config_manager.get("interval_minutes", 30))
            next_change = last_change_dt + interval
            time_remaining = next_change - datetime.now()
            
            return max(0, int(time_remaining.total_seconds()))
        except:
            return None
    
    def set_countdown_callback(self, callback: Callable) -> None:
        """
        Establece el callback para actualizar el contador
        
        Args:
            callback: Función que recibe (minutos, segundos)
        """
        self.countdown_callback = callback
    
    def start_monitoring(self) -> None:
        """Inicia el monitoreo automático"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
    
    def stop_monitoring(self) -> None:
        """Detiene el monitoreo automático"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _monitor_loop(self) -> None:
        """Loop principal de monitoreo"""
        while self.running:
            # Verificar si debe cambiar
            if self.should_change_wallpaper():
                self.change_wallpaper()
            
            # Actualizar contador si está en modo tiempo
            if self.countdown_callback and self.config_manager.get("mode") == "time":
                seconds_remaining = self.get_time_until_next_change()
                if seconds_remaining is not None:
                    minutes = seconds_remaining // 60
                    seconds = seconds_remaining % 60
                    self.countdown_callback(minutes, seconds)
            
            time.sleep(1)  # Verificar cada segundo para el contador
