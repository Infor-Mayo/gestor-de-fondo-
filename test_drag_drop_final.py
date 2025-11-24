"""
Prueba final de drag & drop - Implementación más simple
"""

import tkinter as tk
import customtkinter as ctk
import os
from pathlib import Path

try:
    import tkinterdnd2 as tkdnd
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

def process_dropped_files(files):
    """Procesa archivos arrastrados"""
    print(f"📁 Archivos recibidos: {len(files)}")
    
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.mp4', '.avi', '.mov', '.wmv', '.mkv'}
    valid_files = []
    
    for file_path in files:
        # Limpiar ruta
        file_path = file_path.strip('{}').strip('"').strip("'")
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            ext = Path(file_path).suffix.lower()
            if ext in valid_extensions:
                valid_files.append(file_path)
                file_type = "🎬" if ext in {'.mp4', '.avi', '.mov', '.wmv', '.mkv'} else "🖼️"
                print(f"  ✅ {file_type} {os.path.basename(file_path)}")
            else:
                print(f"  ❌ {os.path.basename(file_path)} (formato no soportado)")
    
    return valid_files

def on_drop(event):
    """Maneja archivos soltados"""
    try:
        files = event.widget.tk.splitlist(event.data)
        valid_files = process_dropped_files(files)
        
        if valid_files:
            # Simular agregar a lista
            textbox = event.widget
            current_text = textbox.get("1.0", tk.END)
            
            # Limpiar texto de ayuda si existe
            if "Arrastra archivos aquí" in current_text:
                textbox.delete("1.0", tk.END)
            
            # Agregar archivos
            for i, file_path in enumerate(valid_files, 1):
                filename = os.path.basename(file_path)
                ext = Path(file_path).suffix.lower()
                icon = "🎬" if ext in {'.mp4', '.avi', '.mov', '.wmv', '.mkv'} else "🖼️"
                textbox.insert(tk.END, f"{i}. {icon} {filename}\n")
            
            print(f"✅ {len(valid_files)} archivo(s) agregado(s)")
        
        # Restaurar color
        event.widget.configure(bg='white')
        
    except Exception as e:
        print(f"❌ Error: {e}")

def on_drag_enter(event):
    """Cambiar color al entrar"""
    try:
        event.widget.configure(bg='lightgreen')
    except:
        pass

def on_drag_leave(event):
    """Restaurar color al salir"""
    try:
        event.widget.configure(bg='white')
    except:
        pass

def create_test_app():
    """Crea aplicación de prueba"""
    
    if DND_AVAILABLE:
        # Usar tkinterdnd2 si está disponible
        root = tkdnd.Tk()
        dnd_status = "✅ tkinterdnd2 disponible"
    else:
        root = tk.Tk()
        dnd_status = "❌ tkinterdnd2 no disponible"
    
    root.title("Prueba Final Drag & Drop")
    root.geometry("500x400")
    
    # Etiqueta de estado
    status_label = tk.Label(root, text=dnd_status, font=('Arial', 10))
    status_label.pack(pady=5)
    
    # Área de texto para drag & drop
    text_area = tk.Text(
        root,
        height=15,
        width=60,
        bg='white',
        relief='sunken',
        bd=2
    )
    text_area.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Texto inicial
    text_area.insert("1.0", 
        "🖱️ Arrastra archivos aquí desde el Explorador de Windows\n\n"
        "📁 Formatos soportados:\n"
        "   • Imágenes: JPG, PNG, BMP\n"
        "   • Videos: MP4, AVI, MOV, WMV, MKV\n\n"
        "💡 Si no funciona:\n"
        "   • Verifica que tkinterdnd2 esté instalado\n"
        "   • Usa clic derecho para opciones alternativas"
    )
    
    if DND_AVAILABLE:
        try:
            # Configurar drag & drop
            text_area.drop_target_register(tkdnd.DND_FILES)
            text_area.dnd_bind('<<Drop>>', on_drop)
            text_area.dnd_bind('<<DragEnter>>', on_drag_enter)
            text_area.dnd_bind('<<DragLeave>>', on_drag_leave)
            
            print("✅ Drag & drop configurado correctamente")
            
        except Exception as e:
            print(f"❌ Error configurando drag & drop: {e}")
    
    # Botón de prueba
    test_btn = tk.Button(
        root,
        text="🧪 Simular archivos arrastrados",
        command=lambda: process_dropped_files([
            "C:/test/imagen.jpg",
            "C:/test/video.mp4",
            "C:/test/documento.txt"
        ])
    )
    test_btn.pack(pady=5)
    
    return root

if __name__ == "__main__":
    print("🧪 PRUEBA FINAL DE DRAG & DROP")
    print("=" * 50)
    
    app = create_test_app()
    
    print("🎯 Aplicación lista. Prueba arrastrando archivos.")
    print("💡 Cierra la ventana para terminar.")
    
    app.mainloop()
    
    print("👋 Prueba terminada.")
