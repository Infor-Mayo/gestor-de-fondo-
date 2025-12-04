"""
Módulo de gestión de configuración
Maneja la carga, guardado y validación de la configuración
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigManager:
    """Gestiona la configuración de la aplicación"""
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Inicializa el gestor de configuración
        
        Args:
            config_file: Ruta al archivo de configuración. Si es None, usa la ubicación por defecto
        """
        if config_file is None:
            self.config_file = Path.home() / "wallpaper_changer_config.json"
        else:
            self.config_file = config_file
        
        self.config = self.load_config()
    
    def get_default_config(self) -> Dict[str, Any]:
        """Retorna la configuración por defecto"""
        return {
            "mode": "time",  # "time" o "weekday"
            "interval_minutes": 30,
            "wallpapers": [],
            "wallpaper_folder": None,
            "use_folder": False,
            # Compatibilidad: fondo único por día (legacy)
            "weekday_wallpapers": {
                "0": None,  # Lunes
                "1": None,  # Martes
                "2": None,  # Miércoles
                "3": None,  # Jueves
                "4": None,  # Viernes
                "5": None,  # Sábado
                "6": None   # Domingo
            },
            # Nuevo: playlist por día y rotación intra-día
            "weekday_playlists": {
                "0": {"use_folder": False, "folder": None, "wallpapers": []},
                "1": {"use_folder": False, "folder": None, "wallpapers": []},
                "2": {"use_folder": False, "folder": None, "wallpapers": []},
                "3": {"use_folder": False, "folder": None, "wallpapers": []},
                "4": {"use_folder": False, "folder": None, "wallpapers": []},
                "5": {"use_folder": False, "folder": None, "wallpapers": []},
                "6": {"use_folder": False, "folder": None, "wallpapers": []}
            },
            "weekday_rotation_minutes": 30,
            "last_change": None,
            "current_index": 0
        }
    
    def load_config(self) -> Dict[str, Any]:
        """Carga la configuración desde el archivo JSON"""
        default_config = self.get_default_config()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error cargando configuración: {e}")
        
        return default_config
    
    def save_config(self) -> bool:
        """
        Guarda la configuración en el archivo JSON
        
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando configuración: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de la configuración"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Establece un valor en la configuración"""
        self.config[key] = value
    
    def update(self, updates: Dict[str, Any]) -> None:
        """Actualiza múltiples valores de la configuración"""
        self.config.update(updates)
