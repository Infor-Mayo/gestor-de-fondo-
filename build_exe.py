"""
Script para compilar la aplicación a EXE con PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """Compila la aplicación a EXE"""
    print("🔨 COMPILANDO APLICACIÓN A EXE")
    print("=" * 40)
    
    try:
        # Verificar que PyInstaller esté instalado
        try:
            import PyInstaller
            print(f"✅ PyInstaller encontrado: {PyInstaller.__version__}")
        except ImportError:
            print("❌ PyInstaller no está instalado")
            print("💡 Instálalo con: pip install pyinstaller")
            return False
        
        # Configuración de PyInstaller
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "main.py")
        
        # Verificar archivos necesarios
        modules_dir = os.path.join(script_dir, "modules")
        config_file = os.path.join(script_dir, "config.json")
        
        if not os.path.exists(modules_dir):
            print("❌ Directorio 'modules' no encontrado")
            return False
            
        if not os.path.exists(config_file):
            print("⚠️ config.json no encontrado, creando uno básico...")
            # Crear config básico si no existe
            basic_config = {
                "mode": "time",
                "interval": 30,
                "wallpapers": [],
                "use_folder": False,
                "wallpaper_folder": "",
                "last_change": "Nunca"
            }
            import json
            with open(config_file, 'w') as f:
                json.dump(basic_config, f, indent=2)
        
        # Comando de PyInstaller
        cmd = [
            "pyinstaller",
            "--onefile",                    # Un solo archivo EXE
            "--windowed",                   # Sin ventana de consola
            "--name=CambiadorFondo",        # Nombre del EXE
            "--add-data=modules;modules",   # Incluir módulos
            "--add-data=config.json;.",     # Incluir configuración
            "--add-data=assets;assets",     # Incluir assets (iconos)
            "--hidden-import=tkinterdnd2",  # Importaciones ocultas
            "--hidden-import=PIL",
            "--hidden-import=Pillow",
            "--hidden-import=cv2",
            "--hidden-import=numpy",
            "--hidden-import=customtkinter",
            "--hidden-import=darkdetect",
            "--hidden-import=pystray",
            "--hidden-import=PIL.Image",
            "--hidden-import=PIL.ImageTk",
            "--hidden-import=tkinter",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=winreg",
            "--collect-all=customtkinter",  # Incluir todos los archivos de customtkinter
            "--collect-all=pystray",        # Incluir todos los archivos de pystray
            "--clean",                      # Limpiar cache
            main_script
        ]
        
        # Agregar icono si existe
        icon_file = os.path.join(script_dir, "assets", "icon.ico")
        if os.path.exists(icon_file):
            cmd.insert(-1, f"--icon={icon_file}")
            print(f"✅ Icono encontrado: {icon_file}")
        else:
            print("⚠️ Icono no encontrado, usando icono por defecto")
        
        print("🔧 Ejecutando PyInstaller...")
        print(f"📁 Directorio: {script_dir}")
        print(f"📄 Script principal: {main_script}")
        
        # Ejecutar PyInstaller
        result = subprocess.run(cmd, cwd=script_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Compilación exitosa!")
            
            # Buscar el EXE generado
            dist_dir = os.path.join(script_dir, "dist")
            exe_path = os.path.join(dist_dir, "CambiadorFondo.exe")
            
            if os.path.exists(exe_path):
                exe_size = os.path.getsize(exe_path) / (1024 * 1024)  # MB
                print(f"📦 EXE generado: {exe_path}")
                print(f"📏 Tamaño: {exe_size:.1f} MB")
                
                # Probar el EXE
                print("\n🧪 Probando EXE...")
                test_result = subprocess.run([exe_path, "--help"], capture_output=True, text=True, timeout=10)
                
                if test_result.returncode == 0:
                    print("✅ EXE funciona correctamente")
                else:
                    print("⚠️ EXE compilado pero puede tener problemas")
                
                return True
            else:
                print("❌ EXE no encontrado en dist/")
                return False
        else:
            print("❌ Error en la compilación:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def create_installer():
    """Crea un instalador con NSIS (opcional)"""
    print("\n📦 CREANDO INSTALADOR")
    print("=" * 30)
    
    try:
        # Verificar si NSIS está disponible
        nsis_path = r"C:\Program Files (x86)\NSIS\makensis.exe"
        if not os.path.exists(nsis_path):
            print("⚠️ NSIS no encontrado, saltando creación de instalador")
            print("💡 Instala NSIS desde: https://nsis.sourceforge.io/")
            return False
        
        # Crear script NSI básico
        nsi_content = '''
!define APP_NAME "Cambiador de Fondo"
!define APP_VERSION "2.0"
!define APP_PUBLISHER "Cambiador de Fondo Team"
!define APP_EXE "CambiadorFondo.exe"

OutFile "CambiadorFondo_Installer.exe"
InstallDir "$PROGRAMFILES\\${APP_NAME}"

Page directory
Page instfiles

Section "Install"
    SetOutPath $INSTDIR
    File "dist\\${APP_EXE}"
    
    ; Crear acceso directo en el escritorio
    CreateShortCut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    
    ; Crear acceso directo en el menú inicio
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    CreateShortCut "$SMPROGRAMS\\${APP_NAME}\\Desinstalar.lnk" "$INSTDIR\\uninstall.exe"
    
    ; Crear desinstalador
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\${APP_EXE}"
    Delete "$INSTDIR\\uninstall.exe"
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\\${APP_NAME}\\Desinstalar.lnk"
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    RMDir "$INSTDIR"
SectionEnd
'''
        
        # Escribir archivo NSI
        nsi_file = "installer.nsi"
        with open(nsi_file, 'w', encoding='utf-8') as f:
            f.write(nsi_content)
        
        # Compilar instalador
        result = subprocess.run([nsis_path, nsi_file], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Instalador creado: CambiadorFondo_Installer.exe")
            return True
        else:
            print("❌ Error creando instalador:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 CONSTRUCTOR DE APLICACIÓN")
    print("=" * 50)
    
    # Compilar EXE
    if build_exe():
        print("\n🎉 ¡EXE compilado exitosamente!")
        
        # Omitir creación de instalador automáticamente
        # response = input("\n¿Crear instalador? (s/n): ").lower().strip()
        # if response in ['s', 'si', 'sí', 'y', 'yes']:
        #     create_installer()
        
        print("\n📋 ARCHIVOS GENERADOS:")
        print("  📦 dist/CambiadorFondo.exe - Aplicación ejecutable")
        print("  📄 CambiadorFondo.spec - Configuración de PyInstaller")
        if os.path.exists("CambiadorFondo_Installer.exe"):
            print("  💿 CambiadorFondo_Installer.exe - Instalador")
        
        print("\n💡 SIGUIENTE PASO:")
        print("  Ejecuta 'python install_context_menu.py' desde el EXE")
        print("  para instalar el menú contextual dinámicamente.")
        
    else:
        print("\n❌ Error compilando EXE")

if __name__ == "__main__":
    main()
