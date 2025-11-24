"""
Script para agregar archivos a la lista de fondos desde el menú contextual
"""

import os
import sys
from pathlib import Path

def add_file_to_wallpaper_list(file_path):
    """Agrega un archivo a la lista de fondos de pantalla"""
    try:
        # Agregar módulos al path
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.append(os.path.join(script_dir, 'modules'))
        
        from modules.config_manager import ConfigManager
        from modules.video_wallpaper import VideoWallpaperEngine
        
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            show_message("Error", f"El archivo no existe:\n{file_path}")
            return False
        
        # Verificar extensión
        ext = Path(file_path).suffix.lower()
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        
        if ext not in valid_extensions:
            show_message("Formato No Soportado", f"Formato de archivo no soportado: {ext}")
            return False
        
        # Cargar configuración
        config = ConfigManager()
        wallpapers = config.get("wallpapers", [])
        
        # Verificar si ya existe
        if file_path in wallpapers:
            show_message("Ya Existe", f"El archivo ya está en la lista de fondos:\n{os.path.basename(file_path)}")
            return False
        
        # Agregar archivo
        wallpapers.append(file_path)
        config.set("wallpapers", wallpapers)
        config.save_config()
        
        # Determinar tipo
        video_engine = VideoWallpaperEngine()
        file_type = "🎬 Video" if video_engine.is_video_file(file_path) else "🖼️ Imagen"
        
        show_message("Agregado Exitosamente", 
                    f"✅ {file_type} agregado a la lista de fondos:\n\n"
                    f"{os.path.basename(file_path)}\n\n"
                    f"Total de archivos: {len(wallpapers)}")
        
        return True
        
    except Exception as e:
        show_message("Error", f"Error agregando archivo:\n{str(e)}")
        return False

def show_message(title, message):
    """Muestra un mensaje al usuario"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        
        # Mostrar mensaje
        messagebox.showinfo(title, message)
        
        root.destroy()
        
    except Exception:
        # Fallback: usar print si no hay GUI disponible
        print(f"{title}: {message}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        show_message("Error", "Uso: python add_to_wallpaper_list.py <archivo>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    success = add_file_to_wallpaper_list(file_path)
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)
