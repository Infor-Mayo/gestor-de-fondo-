"""
Prueba simple de drag & drop para verificar funcionalidad
"""

import tkinter as tk
from tkinter import messagebox
import os
from pathlib import Path

try:
    import tkinterdnd2 as tkdnd
    DND_AVAILABLE = True
    print("✅ tkinterdnd2 disponible")
except ImportError:
    DND_AVAILABLE = False
    print("❌ tkinterdnd2 no disponible")

def process_files(files):
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
                print(f"  {file_type} {os.path.basename(file_path)}")
    
    if valid_files:
        messagebox.showinfo("Éxito", f"Se procesaron {len(valid_files)} archivo(s) válido(s)")
    else:
        messagebox.showwarning("Sin archivos", "No se encontraron archivos válidos")

def on_drop(event):
    """Maneja archivos soltados"""
    try:
        files = event.widget.tk.splitlist(event.data)
        process_files(files)
    except Exception as e:
        print(f"Error: {e}")

def on_drag_enter(event):
    """Cambiar apariencia al entrar"""
    event.widget.configure(bg='lightgreen')

def on_drag_leave(event):
    """Restaurar apariencia al salir"""
    event.widget.configure(bg='white')

def create_test_window():
    """Crea ventana de prueba"""
    if DND_AVAILABLE:
        root = tkdnd.Tk()
    else:
        root = tk.Tk()
    
    root.title("Prueba Drag & Drop")
    root.geometry("400x300")
    
    # Crear área de drop
    label = tk.Label(
        root,
        text="🖱️ Arrastra archivos aquí\n\nFormatos soportados:\n• Imágenes: JPG, PNG, BMP\n• Videos: MP4, AVI, MOV, WMV, MKV",
        bg='white',
        relief='sunken',
        bd=2,
        font=('Arial', 12),
        justify='center'
    )
    label.pack(fill='both', expand=True, padx=20, pady=20)
    
    if DND_AVAILABLE:
        # Configurar drag & drop
        label.drop_target_register(tkdnd.DND_FILES)
        label.dnd_bind('<<Drop>>', on_drop)
        label.dnd_bind('<<DragEnter>>', on_drag_enter)
        label.dnd_bind('<<DragLeave>>', on_drag_leave)
        
        status_label = tk.Label(root, text="✅ Drag & Drop activo", fg='green')
    else:
        status_label = tk.Label(root, text="❌ Drag & Drop no disponible", fg='red')
    
    status_label.pack(pady=10)
    
    # Botón de prueba
    test_btn = tk.Button(
        root,
        text="🧪 Probar con archivos simulados",
        command=lambda: process_files([
            "C:/test/image.jpg",
            "C:/test/video.mp4",
            "C:/test/document.txt"
        ])
    )
    test_btn.pack(pady=10)
    
    return root

if __name__ == "__main__":
    print("🧪 PRUEBA SIMPLE DE DRAG & DROP")
    print("=" * 40)
    
    root = create_test_window()
    
    print("🎯 Ventana creada. Prueba arrastrando archivos.")
    print("💡 Cierra la ventana para terminar.")
    
    root.mainloop()
    
    print("👋 Prueba terminada.")
