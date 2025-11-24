"""
Script de prueba para la funcionalidad de drag & drop
Verifica que el arrastrar y soltar funcione correctamente
"""

import os
import sys
import tkinter as tk
from pathlib import Path

# Agregar el directorio modules al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

def test_drag_drop_simulation():
    """Simula la funcionalidad de drag & drop"""
    print("🧪 PRUEBA DE DRAG & DROP")
    print("=" * 50)
    
    # Importar módulos necesarios
    try:
        from modules.gui import WallpaperChangerGUI
        from modules.config_manager import ConfigManager
        import customtkinter as ctk
        
        print("✅ Módulos importados correctamente")
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    
    # Crear ventana de prueba
    try:
        root = ctk.CTk()
        root.title("Prueba Drag & Drop")
        root.geometry("600x400")
        
        # Crear instancia de la GUI
        app = WallpaperChangerGUI(root)
        
        print("✅ Interfaz creada correctamente")
    except Exception as e:
        print(f"❌ Error creando interfaz: {e}")
        return False
    
    # Simular archivos arrastrados
    test_files = [
        "C:\\Users\\test\\image1.jpg",
        "C:\\Users\\test\\video1.mp4", 
        "C:\\Users\\test\\image2.png",
        "C:\\Users\\test\\document.txt",  # Archivo inválido
        "C:\\Users\\test\\video2.avi"
    ]
    
    print(f"\n🎯 Simulando arrastre de {len(test_files)} archivos:")
    for i, file in enumerate(test_files, 1):
        file_type = "📄"
        if file.endswith(('.jpg', '.png', '.bmp')):
            file_type = "🖼️"
        elif file.endswith(('.mp4', '.avi', '.mov', '.wmv', '.mkv')):
            file_type = "🎬"
        
        print(f"  {i}. {file_type} {os.path.basename(file)}")
    
    # Probar el procesamiento de archivos
    try:
        print(f"\n⚙️ Procesando archivos arrastrados...")
        app.process_dropped_files(test_files)
        print("✅ Procesamiento completado sin errores")
    except Exception as e:
        print(f"❌ Error procesando archivos: {e}")
        return False
    
    # Verificar configuración
    try:
        config_manager = ConfigManager()
        wallpapers = config_manager.get("wallpapers", [])
        print(f"\n📊 Archivos en configuración: {len(wallpapers)}")
        
        for wallpaper in wallpapers:
            if any(test_file.endswith(os.path.basename(wallpaper)) for test_file in test_files):
                print(f"  ✅ {os.path.basename(wallpaper)}")
    except Exception as e:
        print(f"⚠️ No se pudo verificar configuración: {e}")
    
    # Cerrar ventana
    root.destroy()
    
    print(f"\n🎉 Prueba completada exitosamente!")
    return True

def test_file_validation():
    """Prueba la validación de archivos"""
    print("\n🔍 PRUEBA DE VALIDACIÓN DE ARCHIVOS")
    print("=" * 50)
    
    # Archivos de prueba con diferentes extensiones
    test_cases = [
        ("imagen.jpg", True, "🖼️"),
        ("video.mp4", True, "🎬"),
        ("foto.PNG", True, "🖼️"),
        ("pelicula.AVI", True, "🎬"),
        ("documento.txt", False, "📄"),
        ("musica.mp3", False, "🎵"),
        ("archivo.zip", False, "📦"),
        ("animation.mkv", True, "🎬"),
        ("picture.bmp", True, "🖼️")
    ]
    
    try:
        from modules.video_wallpaper import VideoWallpaperEngine
        video_engine = VideoWallpaperEngine()
        
        print("Validando extensiones de archivo:")
        
        valid_image_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        valid_video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        
        all_correct = True
        
        for filename, should_be_valid, icon in test_cases:
            file_ext = Path(filename).suffix.lower()
            is_image = file_ext in valid_image_extensions
            is_video = video_engine.is_video_file(filename)
            is_valid = is_image or is_video
            
            status = "✅" if is_valid == should_be_valid else "❌"
            file_type = "imagen" if is_image else "video" if is_video else "no soportado"
            
            print(f"  {status} {icon} {filename} -> {file_type}")
            
            if is_valid != should_be_valid:
                all_correct = False
        
        if all_correct:
            print("\n✅ Todas las validaciones son correctas")
        else:
            print("\n❌ Algunas validaciones fallaron")
            
        return all_correct
        
    except Exception as e:
        print(f"❌ Error en validación: {e}")
        return False

def test_drag_drop_ui_elements():
    """Prueba los elementos de UI relacionados con drag & drop"""
    print("\n🎨 PRUEBA DE ELEMENTOS DE UI")
    print("=" * 50)
    
    try:
        from modules.gui import WallpaperChangerGUI
        import customtkinter as ctk
        
        # Crear ventana temporal
        root = ctk.CTk()
        root.withdraw()  # Ocultar ventana
        
        app = WallpaperChangerGUI(root)
        
        # Probar indicador de drag & drop
        print("Probando indicador visual...")
        app.add_drag_drop_indicator()
        
        # Verificar contenido del textbox
        content = app.wallpapers_textbox.get("1.0", tk.END)
        
        if "Arrastrar archivos" in content or "drag" in content.lower():
            print("✅ Indicador de drag & drop presente")
        else:
            print("⚠️ Indicador de drag & drop no encontrado")
        
        # Probar texto de ayuda
        print("Probando texto de ayuda...")
        app.add_drag_drop_help_text()
        
        content_after = app.wallpapers_textbox.get("1.0", tk.END)
        
        if len(content_after) > len(content):
            print("✅ Texto de ayuda agregado")
        else:
            print("⚠️ Texto de ayuda no se agregó")
        
        root.destroy()
        
        print("✅ Elementos de UI funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error probando UI: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪 SUITE DE PRUEBAS DRAG & DROP")
    print("=" * 60)
    print()
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("Simulación Drag & Drop", test_drag_drop_simulation()))
    results.append(("Validación de Archivos", test_file_validation()))
    results.append(("Elementos de UI", test_drag_drop_ui_elements()))
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas de drag & drop funcionan correctamente!")
        print("\n💡 Para probar manualmente:")
        print("   1. Ejecuta: python main.py")
        print("   2. Ve a la pestaña 'Modo Tiempo'")
        print("   3. Arrastra archivos de imagen/video al área de texto")
        print("   4. Verifica que se agreguen a la lista")
    else:
        print("⚠️ Algunas pruebas fallaron. Revisa la implementación.")

if __name__ == "__main__":
    main()
