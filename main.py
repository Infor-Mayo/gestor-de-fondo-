"""
Cambiador de Fondo de Pantalla - Aplicación Principal
Versión 2.0 - Modular

Aplicación para cambiar automáticamente el fondo de pantalla de Windows
según intervalos de tiempo o días de la semana.

Autor: Cambiador de Fondo Team
Licencia: MIT
"""
import os
import sys
import traceback
from pathlib import Path
import customtkinter as ctk

# Configurar codificación UTF-8 para evitar errores con emojis en Windows
if sys.platform == 'win32':
    try:
        # Verificar que stdout y stderr existan antes de reconfigurar
        if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr is not None and hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except (AttributeError, ValueError, TypeError):
        # Si reconfigure no está disponible, usar código alternativo
        try:
            import io
            if sys.stdout is not None and hasattr(sys.stdout, 'buffer'):
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            if sys.stderr is not None and hasattr(sys.stderr, 'buffer'):
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except (AttributeError, ValueError, TypeError):
            # Si todo falla, simplemente continuar sin reconfigurar
            pass

# Intentar importar tkinterdnd2 para drag & drop
try:
    import tkinterdnd2 as tkdnd
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

# Importar módulos
from modules.gui import WallpaperChangerGUI


def add_wallpaper_from_context_menu(file_path):
    """Agrega un archivo a la lista de fondos desde el menú contextual"""
    try:
        from modules.config_manager import ConfigManager
        from modules.video_wallpaper import VideoWallpaperEngine
        
        # Verificar que el archivo existe
        if not os.path.exists(file_path):
            show_context_message("Error", f"El archivo no existe:\n{file_path}")
            return False
        
        # Verificar extensión
        ext = Path(file_path).suffix.lower()
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        
        if ext not in valid_extensions:
            show_context_message("Formato No Soportado", f"Formato de archivo no soportado: {ext}")
            return False
        
        # Cargar configuración
        config = ConfigManager()
        wallpapers = config.get("wallpapers", [])
        
        # Verificar si ya existe
        if file_path in wallpapers:
            show_context_message("Ya Existe", f"El archivo ya está en la lista de fondos:\n{os.path.basename(file_path)}")
            return False
        
        # Agregar archivo
        wallpapers.append(file_path)
        config.set("wallpapers", wallpapers)
        config.save_config()
        
        # Determinar tipo
        video_engine = VideoWallpaperEngine()
        file_type = "[Video]" if video_engine.is_video_file(file_path) else "[Imagen]"
        
        show_context_message("Agregado Exitosamente", 
                    f"{file_type} agregado a la lista de fondos:\n\n"
                    f"{os.path.basename(file_path)}\n\n"
                    f"Total de archivos: {len(wallpapers)}")
        
        return True
        
    except Exception as e:
        show_context_message("Error", f"Error agregando archivo:\n{str(e)}")
        return False

def show_context_message(title, message):
    """Muestra un mensaje al usuario desde el contexto"""
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        # Crear ventana temporal
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana principal
        root.attributes('-topmost', True)  # Mantener al frente
        
        # Mostrar mensaje
        messagebox.showinfo(title, message)
        
        root.destroy()
        
    except Exception:
        # Fallback: usar print si no hay GUI disponible
        print(f"{title}: {message}")

def main():
    """Función principal de la aplicación"""
    try:
        # Verificar si se está ejecutando desde menú contextual
        if len(sys.argv) > 1 and sys.argv[1] == "--add-wallpaper":
            if len(sys.argv) > 2:
                file_path = sys.argv[2]
                success = add_wallpaper_from_context_menu(file_path)
                sys.exit(0 if success else 1)
            else:
                print("[ERROR] No se especifico archivo")
                sys.exit(1)
        
        # Ejecución normal de la aplicación
        print("[INFO] Iniciando aplicacion...")
        
        # Crear ventana principal con soporte de drag & drop
        print("[INFO] Creando ventana principal...")
        if DND_AVAILABLE:
            print("[INFO] Drag & Drop disponible con tkinterdnd2")
            root = tkdnd.Tk()
            root.withdraw()  # Ocultar temporalmente
            root = ctk.CTk()  # Crear ventana CTk normal
        else:
            print("[ADVERTENCIA] Drag & Drop limitado - tkinterdnd2 no disponible")
            root = ctk.CTk()
        
        # Inicializar aplicación
        print("[INFO] Inicializando GUI...")
        app = WallpaperChangerGUI(root)
        
        print("[INFO] Aplicacion inicializada correctamente")
        print("[INFO] Iniciando loop principal...")
        print("[INFO] La aplicacion seguira ejecutandose en segundo plano cuando se cierre la ventana")
        
        # Iniciar loop principal
        # El mainloop continuará ejecutándose incluso cuando la ventana esté oculta (withdraw)
        # Solo se cerrará cuando se llame a root.destroy() desde quit_app()
        root.mainloop()
        
        print("[INFO] Aplicacion cerrada normalmente")
        
    except ImportError as e:
        print(f"[ERROR] Error de importacion: {e}")
        print("[INFO] Asegurate de que todas las dependencias estan instaladas:")
        print("   pip install -r requirements.txt")
        input("Presiona Enter para continuar...")
        sys.exit(1)
        
    except Exception as e:
        print(f"[ERROR] Error fatal en la aplicacion: {e}")
        print("[INFO] Detalles del error:")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para continuar...")
        sys.exit(1)


if __name__ == "__main__":
    main()
