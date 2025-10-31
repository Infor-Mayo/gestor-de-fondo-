"""Script para convertir la interfaz a CustomTkinter"""
import re

# Leer el archivo original
with open('wallpaper_changer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Reemplazos básicos
replacements = [
    # ttk widgets a ctk widgets
    (r'ttk\.Frame\(', 'ctk.CTkFrame('),
    (r'ttk\.Label\(', 'ctk.CTkLabel('),
    (r'ttk\.Button\(', 'ctk.CTkButton('),
    (r'ttk\.Entry\(', 'ctk.CTkEntry('),
    (r'ttk\.Radiobutton\(', 'ctk.CTkRadioButton('),
    (r'ttk\.Spinbox\(', 'ctk.CTkEntry('),  # CTk no tiene Spinbox
    (r'ttk\.LabelFrame\(', 'ctk.CTkFrame('),
    (r'ttk\.Notebook\(', 'ctk.CTkTabview('),
    (r'tk\.Listbox\(', 'ctk.CTkTextbox('),
    (r'ttk\.Scrollbar\(', '# Scrollbar not needed in CTk'),
    (r'ttk\.Checkbutton\(', 'ctk.CTkCheckBox('),
    (r'ttk\.OptionMenu\(', 'ctk.CTkOptionMenu('),
    
    # Parámetros
    (r'padding=\d+', ''),
    (r'text="([^"]+)"', r'text="\1"'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

# Guardar
with open('wallpaper_changer_ctk.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Conversión completada: wallpaper_changer_ctk.py")
