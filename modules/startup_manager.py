"""
Módulo de gestión de inicio automático
Maneja la configuración de inicio con Windows
"""

import os
import sys
import winreg
from typing import Tuple


class StartupManager:
    """Gestiona el inicio automático con Windows"""
    
    REGISTRY_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
    APP_NAME = "WallpaperChanger"
    
    @staticmethod
    def get_app_path() -> str:
        """
        Obtiene la ruta de la aplicación
        
        Returns:
            Ruta completa de la aplicación
        """
        if getattr(sys, 'frozen', False):
            # Si está compilado como .exe
            return sys.executable
        else:
            # Si se ejecuta como script
            return f'pythonw.exe "{os.path.abspath(sys.argv[0])}"'
    
    @staticmethod
    def is_enabled() -> bool:
        """
        Verifica si el inicio automático está habilitado
        
        Returns:
            True si está habilitado, False en caso contrario
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_READ
            )
            
            try:
                winreg.QueryValueEx(key, StartupManager.APP_NAME)
                winreg.CloseKey(key)
                return True
            except FileNotFoundError:
                winreg.CloseKey(key)
                return False
        except Exception:
            return False
    
    @staticmethod
    def enable() -> Tuple[bool, str]:
        """
        Habilita el inicio automático
        
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            app_path = StartupManager.get_app_path()
            winreg.SetValueEx(key, StartupManager.APP_NAME, 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            
            return True, "Inicio automático habilitado correctamente"
        except Exception as e:
            return False, f"Error al habilitar inicio automático: {e}"
    
    @staticmethod
    def disable() -> Tuple[bool, str]:
        """
        Deshabilita el inicio automático
        
        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                StartupManager.REGISTRY_KEY,
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, StartupManager.APP_NAME)
            except FileNotFoundError:
                pass
            
            winreg.CloseKey(key)
            
            return True, "Inicio automático deshabilitado correctamente"
        except Exception as e:
            return False, f"Error al deshabilitar inicio automático: {e}"
    
    @staticmethod
    def get_status() -> Tuple[bool, str, str]:
        """
        Obtiene el estado del inicio automático
        
        Returns:
            Tupla (habilitado, texto_estado, color)
        """
        if StartupManager.is_enabled():
            return True, "✓ Inicio automático HABILITADO", "green"
        else:
            return False, "✗ Inicio automático DESHABILITADO", "red"
