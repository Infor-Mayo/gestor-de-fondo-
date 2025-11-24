"""
Instala menú contextual en el explorador de Windows para agregar fondos de pantalla
"""

import os
import sys
import winreg
from pathlib import Path

def install_context_menu():
    """Instala el menú contextual en el registro de Windows (versión dinámica)"""
    try:
        # Detectar si estamos en EXE o script Python
        if getattr(sys, 'frozen', False):
            # Ejecutándose como EXE
            app_path = sys.executable
            command_template = f'"{app_path}" --add-wallpaper "%1"'
            print("🔧 Detectado: Aplicación compilada (EXE)")
        else:
            # Ejecutándose como script Python
            script_dir = os.path.dirname(os.path.abspath(__file__))
            main_script = os.path.join(script_dir, "main.py")
            
            # Buscar Python en el sistema
            python_exe = find_python_executable()
            if not python_exe:
                print("❌ No se encontró Python en el sistema")
                return False
            
            command_template = f'"{python_exe}" "{main_script}" --add-wallpaper "%1"'
            print(f"🔧 Detectado: Script Python con {python_exe}")
        
        # Extensiones de archivos soportadas
        extensions = [
            # Imágenes
            '.jpg', '.jpeg', '.png', '.bmp',
            # Videos
            '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'
        ]
        
        print("🔧 Instalando menú contextual en el registro de Windows...")
        
        for ext in extensions:
            try:
                # Crear clave para la extensión
                key_path = f"SystemFileAssociations\\{ext}\\shell\\AddToWallpaperList"
                
                # Crear clave principal
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                    winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "🖼️ Agregar a Lista de Fondos")
                    # No usar icono específico para mayor compatibilidad
                
                # Crear subclave command
                command_path = f"{key_path}\\command"
                with winreg.CreateKey(winreg.HKEY_CURRENT_USER, command_path) as cmd_key:
                    winreg.SetValueEx(cmd_key, "", 0, winreg.REG_SZ, command_template)
                
                print(f"  ✅ {ext}")
                
            except Exception as e:
                print(f"  ❌ Error con {ext}: {e}")
        
        print("\n🎉 ¡Menú contextual instalado exitosamente!")
        print("💡 Ahora puedes hacer clic derecho en imágenes y videos")
        print("   y seleccionar '🖼️ Agregar a Lista de Fondos'")
        
        return True
        
    except Exception as e:
        print(f"❌ Error instalando menú contextual: {e}")
        return False

def find_python_executable():
    """Busca el ejecutable de Python en el sistema"""
    import shutil
    
    # Intentar encontrar Python en PATH
    python_candidates = ['python', 'python3', 'py']
    
    for candidate in python_candidates:
        python_path = shutil.which(candidate)
        if python_path:
            return python_path
    
    # Buscar en ubicaciones comunes
    common_paths = [
        r"C:\Python*\python.exe",
        r"C:\Users\*\AppData\Local\Programs\Python\Python*\python.exe",
        r"C:\Program Files\Python*\python.exe",
        r"C:\Program Files (x86)\Python*\python.exe"
    ]
    
    import glob
    for pattern in common_paths:
        matches = glob.glob(pattern)
        if matches:
            return matches[0]
    
    return None

def create_add_script(script_path):
    """Crea el script que se ejecutará desde el menú contextual"""
    script_content = '''"""
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
            show_message("Error", f"El archivo no existe:\\n{file_path}")
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
            show_message("Ya Existe", f"El archivo ya está en la lista de fondos:\\n{os.path.basename(file_path)}")
            return False
        
        # Agregar archivo
        wallpapers.append(file_path)
        config.set("wallpapers", wallpapers)
        config.save_config()
        
        # Determinar tipo
        video_engine = VideoWallpaperEngine()
        file_type = "🎬 Video" if video_engine.is_video_file(file_path) else "🖼️ Imagen"
        
        show_message("Agregado Exitosamente", 
                    f"✅ {file_type} agregado a la lista de fondos:\\n\\n"
                    f"{os.path.basename(file_path)}\\n\\n"
                    f"Total de archivos: {len(wallpapers)}")
        
        return True
        
    except Exception as e:
        show_message("Error", f"Error agregando archivo:\\n{str(e)}")
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
'''
    
    # Escribir el script
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"✅ Script creado: {script_path}")

def uninstall_context_menu():
    """Desinstala el menú contextual del registro"""
    try:
        extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v']
        
        print("🗑️ Desinstalando menú contextual...")
        
        for ext in extensions:
            try:
                key_path = f"SystemFileAssociations\\{ext}\\shell\\AddToWallpaperList"
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, f"{key_path}\\command")
                winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
                print(f"  ✅ {ext}")
            except FileNotFoundError:
                print(f"  ⚠️ {ext} (ya no existe)")
            except Exception as e:
                print(f"  ❌ Error con {ext}: {e}")
        
        print("✅ Menú contextual desinstalado")
        return True
        
    except Exception as e:
        print(f"❌ Error desinstalando: {e}")
        return False

def main():
    """Función principal"""
    print("🖼️ INSTALADOR DE MENÚ CONTEXTUAL")
    print("=" * 40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        return uninstall_context_menu()
    
    print("💡 Esto agregará una opción al menú contextual del explorador")
    print("   para agregar imágenes y videos a la lista de fondos.\\n")
    
    response = input("¿Continuar con la instalación? (s/n): ").lower().strip()
    
    if response in ['s', 'si', 'sí', 'y', 'yes']:
        return install_context_menu()
    else:
        print("❌ Instalación cancelada")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\\n🎉 ¡Listo! Prueba hacer clic derecho en una imagen o video.")
        else:
            print("\\n❌ La instalación falló.")
    except KeyboardInterrupt:
        print("\\n❌ Instalación cancelada por el usuario")
    except Exception as e:
        print(f"\\n❌ Error inesperado: {e}")
