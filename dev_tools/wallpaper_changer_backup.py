import os
import json
import ctypes
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk
import winreg
import sys
import pystray
from PIL import Image as PILImage
import io
import darkdetect

class WallpaperChanger:
    def __init__(self):
        self.config_file = Path.home() / "wallpaper_changer_config.json"
        self.config = self.load_config()
        self.running = False
        self.thread = None
        
    def load_config(self):
        """Carga la configuración desde el archivo JSON"""
        default_config = {
            "mode": "time",  # "time" o "weekday"
            "interval_minutes": 30,
            "wallpapers": [],
            "wallpaper_folder": None,  # Carpeta de fondos
            "use_folder": False,  # Usar carpeta en lugar de lista
            "weekday_wallpapers": {
                "0": None,  # Lunes
                "1": None,  # Martes
                "2": None,  # Miércoles
                "3": None,  # Jueves
                "4": None,  # Viernes
                "5": None,  # Sábado
                "6": None   # Domingo
            },
            "last_change": None,
            "current_index": 0
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    default_config.update(loaded_config)
            except Exception as e:
                print(f"Error cargando configuración: {e}")
        
        return default_config
    
    def save_config(self):
        """Guarda la configuración en el archivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuración: {e}")
    
    def set_wallpaper(self, image_path):
        """Cambia el fondo de pantalla en Windows"""
        try:
            # Convertir a ruta absoluta
            abs_path = os.path.abspath(image_path)
            
            # Cambiar el fondo de pantalla
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                abs_path, 
                3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            return True
        except Exception as e:
            print(f"Error cambiando fondo: {e}")
            return False
    
    def get_images_from_folder(self):
        """Obtiene todas las imágenes de la carpeta configurada"""
        if not self.config.get("wallpaper_folder") or not os.path.exists(self.config["wallpaper_folder"]):
            return []
        
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp'}
        images = []
        
        try:
            for file in os.listdir(self.config["wallpaper_folder"]):
                if Path(file).suffix.lower() in valid_extensions:
                    full_path = os.path.join(self.config["wallpaper_folder"], file)
                    images.append(full_path)
        except Exception as e:
            print(f"Error leyendo carpeta: {e}")
        
        return sorted(images)
    
    def get_wallpaper_list(self):
        """Obtiene la lista de fondos según la configuración"""
        if self.config.get("use_folder", False):
            return self.get_images_from_folder()
        else:
            return self.config["wallpapers"]
    
    def get_next_wallpaper_time_mode(self):
        """Obtiene el siguiente fondo en modo tiempo"""
        wallpapers = self.get_wallpaper_list()
        
        if not wallpapers:
            return None
        
        wallpaper = wallpapers[self.config["current_index"]]
        self.config["current_index"] = (self.config["current_index"] + 1) % len(wallpapers)
        self.save_config()
        return wallpaper
    
    def get_wallpaper_for_today(self):
        """Obtiene el fondo para el día actual"""
        weekday = str(datetime.now().weekday())
        return self.config["weekday_wallpapers"].get(weekday)
    
    def should_change_wallpaper(self):
        """Determina si debe cambiar el fondo"""
        if self.config["mode"] == "time":
            if not self.config["last_change"]:
                return True
            
            last_change = datetime.fromisoformat(self.config["last_change"])
            interval = timedelta(minutes=self.config["interval_minutes"])
            return datetime.now() - last_change >= interval
        
        elif self.config["mode"] == "weekday":
            # Verificar si cambió el día
            if not self.config["last_change"]:
                return True
            
            last_change = datetime.fromisoformat(self.config["last_change"])
            return last_change.date() != datetime.now().date()
        
        return False
    
    def change_wallpaper(self):
        """Cambia el fondo de pantalla según la configuración"""
        if self.config["mode"] == "time":
            wallpaper = self.get_next_wallpaper_time_mode()
        else:
            wallpaper = self.get_wallpaper_for_today()
        
        if wallpaper and os.path.exists(wallpaper):
            if self.set_wallpaper(wallpaper):
                self.config["last_change"] = datetime.now().isoformat()
                self.save_config()
                return True
        return False
    
    def start_monitoring(self):
        """Inicia el monitoreo automático"""
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
    
    def stop_monitoring(self):
        """Detiene el monitoreo automático"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _monitor_loop(self):
        """Loop principal de monitoreo"""
        while self.running:
            if self.should_change_wallpaper():
                self.change_wallpaper()
            time.sleep(60)  # Verificar cada minuto


class WallpaperChangerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cambiador de Fondo de Pantalla")
        self.root.geometry("800x650")
        
        # Detectar tema del sistema
        system_theme = darkdetect.theme()
        if system_theme == "Dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        
        ctk.set_default_color_theme("blue")
        
        self.changer = WallpaperChanger()
        self.tray_icon = None
        self.current_theme = ctk.get_appearance_mode()
        
        self.setup_ui()
        self.load_current_config()
        
        # Iniciar monitoreo automático
        self.changer.start_monitoring()
        
        # Configurar system tray
        self.setup_tray_icon()
        
        # Protocolo de cierre
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Header con título y selector de tema
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill='x', pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🖼️ Cambiador de Fondo de Pantalla",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(side='left', padx=15, pady=10)
        
        # Selector de tema
        theme_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        theme_frame.pack(side='right', padx=15)
        
        ctk.CTkLabel(theme_frame, text="Tema:", font=ctk.CTkFont(size=12)).pack(side='left', padx=5)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["System", "Light", "Dark"],
            command=self.change_theme,
            variable=self.theme_var,
            width=120
        )
        theme_menu.pack(side='left', padx=5)
        
        # Tabview para pestañas
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill='both', expand=True)
        
        # Crear pestañas
        self.tabview.add("⚙️ General")
        self.tabview.add("⏰ Modo Tiempo")
        self.tabview.add("📅 Modo Días")
        self.tabview.add("🚀 Inicio Automático")
        
        # Configurar cada pestaña
        self.setup_general_tab(self.tabview.tab("⚙️ General"))
        self.setup_time_tab(self.tabview.tab("⏰ Modo Tiempo"))
        self.setup_weekday_tab(self.tabview.tab("📅 Modo Días"))
        self.setup_startup_tab(self.tabview.tab("🚀 Inicio Automático"))
    
    def setup_general_tab(self, parent):
        """Configura la pestaña general"""
        # Modo de operación
        mode_frame = ttk.LabelFrame(parent, text="Modo de Operación", padding=10)
        mode_frame.pack(fill='x', padx=10, pady=10)
        
        self.mode_var = tk.StringVar(value=self.changer.config["mode"])
        
        ttk.Radiobutton(
            mode_frame, 
            text="Cambiar cada cierto tiempo", 
            variable=self.mode_var, 
            value="time",
            command=self.on_mode_change
        ).pack(anchor='w', pady=5)
        
        ttk.Radiobutton(
            mode_frame, 
            text="Cambiar según día de la semana", 
            variable=self.mode_var, 
            value="weekday",
            command=self.on_mode_change
        ).pack(anchor='w', pady=5)
        
        # Botón de cambio manual
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(fill='x', padx=10, pady=10)
        
        self.change_now_button = ttk.Button(
            btn_frame, 
            text="Cambiar Fondo Ahora", 
            command=self.change_now
        )
        self.change_now_button.pack(pady=5)
        
        # Estado
        status_frame = ttk.LabelFrame(parent, text="Estado", padding=10)
        status_frame.pack(fill='x', padx=10, pady=10)
        
        self.status_label = ttk.Label(status_frame, text="")
        self.status_label.pack()
        
        self.update_status()
    
    def setup_time_tab(self, parent):
        """Configura la pestaña de modo tiempo"""
        # Intervalo
        interval_frame = ttk.LabelFrame(parent, text="Intervalo de Cambio", padding=10)
        interval_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(interval_frame, text="Cambiar cada:").grid(row=0, column=0, sticky='w', pady=5)
        
        self.interval_var = tk.IntVar(value=self.changer.config["interval_minutes"])
        interval_spin = ttk.Spinbox(
            interval_frame, 
            from_=1, 
            to=1440, 
            textvariable=self.interval_var,
            width=10
        )
        interval_spin.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(interval_frame, text="minutos").grid(row=0, column=2, sticky='w', pady=5)
        
        ttk.Button(
            interval_frame, 
            text="Guardar Intervalo", 
            command=self.save_interval
        ).grid(row=1, column=0, columnspan=3, pady=10)
        
        # Carpeta de fondos
        folder_frame = ttk.LabelFrame(parent, text="Carpeta de Fondos (Persistente)", padding=10)
        folder_frame.pack(fill='x', padx=10, pady=10)
        
        self.use_folder_var = tk.BooleanVar(value=self.changer.config.get("use_folder", False))
        
        ttk.Checkbutton(
            folder_frame,
            text="Usar carpeta en lugar de lista manual",
            variable=self.use_folder_var,
            command=self.toggle_folder_mode
        ).pack(anchor='w', pady=5)
        
        folder_select_frame = ttk.Frame(folder_frame)
        folder_select_frame.pack(fill='x', pady=5)
        
        self.folder_entry = ttk.Entry(folder_select_frame, width=40)
        self.folder_entry.pack(side='left', fill='x', expand=True, padx=(0, 5))
        if self.changer.config.get("wallpaper_folder"):
            self.folder_entry.insert(0, self.changer.config["wallpaper_folder"])
        
        ttk.Button(
            folder_select_frame,
            text="Seleccionar Carpeta",
            command=self.select_wallpaper_folder
        ).pack(side='left')
        
        self.folder_info_label = ttk.Label(folder_frame, text="", foreground="blue")
        self.folder_info_label.pack(pady=5)
        self.update_folder_info()
        
        # Lista de fondos
        wallpapers_frame = ttk.LabelFrame(parent, text="Fondos de Pantalla (Lista Manual)", padding=10)
        wallpapers_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Listbox con scrollbar
        list_frame = ttk.Frame(wallpapers_frame)
        list_frame.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side='right', fill='y')
        
        self.wallpapers_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set)
        self.wallpapers_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.wallpapers_listbox.yview)
        
        # Botones
        btn_frame = ttk.Frame(wallpapers_frame)
        btn_frame.pack(fill='x', pady=5)
        
        ttk.Button(btn_frame, text="Agregar Imagen", command=self.add_wallpaper).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Eliminar Seleccionada", command=self.remove_wallpaper).pack(side='left', padx=5)
        ttk.Button(btn_frame, text="Refrescar Lista", command=self.refresh_wallpaper_list).pack(side='left', padx=5)
    
    def setup_weekday_tab(self, parent):
        """Configura la pestaña de días de la semana"""
        info_label = ttk.Label(
            parent, 
            text="Asigna un fondo de pantalla para cada día de la semana:",
            font=('Arial', 10, 'bold')
        )
        info_label.pack(pady=10)
        
        days = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.weekday_entries = {}
        
        for i, day in enumerate(days):
            frame = ttk.Frame(parent)
            frame.pack(fill='x', padx=20, pady=5)
            
            ttk.Label(frame, text=day + ":", width=12).pack(side='left')
            
            entry = ttk.Entry(frame, width=40)
            entry.pack(side='left', padx=5, fill='x', expand=True)
            self.weekday_entries[str(i)] = entry
            
            ttk.Button(
                frame, 
                text="Seleccionar", 
                command=lambda d=str(i): self.select_weekday_wallpaper(d)
            ).pack(side='left', padx=5)
        
        ttk.Button(
            parent, 
            text="Guardar Configuración de Días", 
            command=self.save_weekday_config
        ).pack(pady=20)
    
    def setup_startup_tab(self, parent):
        """Configura la pestaña de inicio automático"""
        info_frame = ttk.LabelFrame(parent, text="Inicio Automático con Windows", padding=20)
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        ttk.Label(
            info_frame,
            text="Configura la aplicación para que se inicie automáticamente\ncuando Windows arranque.",
            justify='center'
        ).pack(pady=10)
        
        self.startup_status_label = ttk.Label(info_frame, text="", font=('Arial', 10, 'bold'))
        self.startup_status_label.pack(pady=10)
        
        btn_frame = ttk.Frame(info_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame,
            text="Habilitar Inicio Automático",
            command=self.enable_startup
        ).pack(side='left', padx=5)
        
        ttk.Button(
            btn_frame,
            text="Deshabilitar Inicio Automático",
            command=self.disable_startup
        ).pack(side='left', padx=5)
        
        self.update_startup_status()
    
    def load_current_config(self):
        """Carga la configuración actual en la interfaz"""
        # Cargar lista de fondos según el modo
        if self.changer.config.get("use_folder", False):
            # Si usa carpeta, mostrar imágenes de la carpeta
            images = self.changer.get_images_from_folder()
            for img in images:
                self.wallpapers_listbox.insert(tk.END, img)
        else:
            # Si usa lista manual, mostrar la lista
            for wallpaper in self.changer.config["wallpapers"]:
                self.wallpapers_listbox.insert(tk.END, wallpaper)
        
        # Cargar fondos por día
        for day, wallpaper in self.changer.config["weekday_wallpapers"].items():
            if wallpaper:
                self.weekday_entries[day].insert(0, wallpaper)
        
        # Configurar estado inicial del botón según el modo
        if self.changer.config["mode"] == "weekday":
            self.change_now_button.config(state="disabled")
        else:
            self.change_now_button.config(state="normal")
    
    def on_mode_change(self):
        """Maneja el cambio de modo"""
        self.changer.config["mode"] = self.mode_var.get()
        self.changer.save_config()
        self.update_status()
        
        # Deshabilitar botón "Cambiar Ahora" en modo días de la semana
        if self.mode_var.get() == "weekday":
            self.change_now_button.config(state="disabled")
        else:
            self.change_now_button.config(state="normal")
        
        messagebox.showinfo("Modo Cambiado", f"Modo cambiado a: {self.mode_var.get()}")
    
    def save_interval(self):
        """Guarda el intervalo de cambio"""
        self.changer.config["interval_minutes"] = self.interval_var.get()
        self.changer.save_config()
        self.update_status()
        messagebox.showinfo("Guardado", "Intervalo guardado correctamente")
    
    def add_wallpaper(self):
        """Agrega un fondo de pantalla a la lista"""
        files = filedialog.askopenfilenames(
            title="Seleccionar imágenes",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.changer.config["wallpapers"]:
                self.changer.config["wallpapers"].append(file)
                self.wallpapers_listbox.insert(tk.END, file)
        
        self.changer.save_config()
    
    def remove_wallpaper(self):
        """Elimina el fondo seleccionado"""
        selection = self.wallpapers_listbox.curselection()
        if selection:
            index = selection[0]
            self.wallpapers_listbox.delete(index)
            del self.changer.config["wallpapers"][index]
            self.changer.save_config()
    
    def select_wallpaper_folder(self):
        """Selecciona una carpeta de fondos"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta con imágenes"
        )
        
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)
            self.changer.config["wallpaper_folder"] = folder
            self.changer.save_config()
            self.update_folder_info()
            messagebox.showinfo("Carpeta Seleccionada", 
                              f"Carpeta configurada correctamente.\n\n{self.folder_info_label.cget('text')}")
    
    def toggle_folder_mode(self):
        """Activa/desactiva el modo de carpeta"""
        self.changer.config["use_folder"] = self.use_folder_var.get()
        self.changer.config["current_index"] = 0  # Reiniciar índice
        self.changer.save_config()
        self.update_folder_info()
        
        mode_text = "carpeta" if self.use_folder_var.get() else "lista manual"
        messagebox.showinfo("Modo Cambiado", f"Ahora se usará: {mode_text}")
    
    def update_folder_info(self):
        """Actualiza la información de la carpeta"""
        if self.changer.config.get("use_folder", False):
            images = self.changer.get_images_from_folder()
            count = len(images)
            self.folder_info_label.config(
                text=f"✓ Modo carpeta activo - {count} imagen(es) encontrada(s)",
                foreground="green"
            )
        else:
            if self.changer.config.get("wallpaper_folder"):
                images = self.changer.get_images_from_folder()
                count = len(images)
                self.folder_info_label.config(
                    text=f"Carpeta configurada - {count} imagen(es) disponible(s) (modo desactivado)",
                    foreground="orange"
                )
            else:
                self.folder_info_label.config(
                    text="No hay carpeta configurada",
                    foreground="gray"
                )
    
    def refresh_wallpaper_list(self):
        """Refresca la lista de fondos mostrada"""
        self.wallpapers_listbox.delete(0, tk.END)
        
        if self.changer.config.get("use_folder", False):
            # Mostrar imágenes de la carpeta
            images = self.changer.get_images_from_folder()
            for img in images:
                self.wallpapers_listbox.insert(tk.END, img)
        else:
            # Mostrar lista manual
            for wallpaper in self.changer.config["wallpapers"]:
                self.wallpapers_listbox.insert(tk.END, wallpaper)
        
        self.update_folder_info()
    
    def select_weekday_wallpaper(self, day):
        """Selecciona un fondo para un día específico"""
        file = filedialog.askopenfilename(
            title=f"Seleccionar fondo para el día",
            filetypes=[
                ("Imágenes", "*.jpg *.jpeg *.png *.bmp"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if file:
            self.weekday_entries[day].delete(0, tk.END)
            self.weekday_entries[day].insert(0, file)
    
    def save_weekday_config(self):
        """Guarda la configuración de días"""
        for day, entry in self.weekday_entries.items():
            value = entry.get()
            self.changer.config["weekday_wallpapers"][day] = value if value else None
        
        self.changer.save_config()
        messagebox.showinfo("Guardado", "Configuración de días guardada correctamente")
    
    def change_now(self):
        """Cambia el fondo inmediatamente"""
        if self.changer.change_wallpaper():
            messagebox.showinfo("Éxito", "Fondo de pantalla cambiado correctamente")
            self.update_status()
        else:
            messagebox.showerror("Error", "No se pudo cambiar el fondo de pantalla")
    
    def update_status(self):
        """Actualiza el estado mostrado"""
        mode = "Tiempo" if self.changer.config["mode"] == "time" else "Días de la semana"
        last_change = self.changer.config.get("last_change", "Nunca")
        
        if last_change != "Nunca":
            try:
                last_change = datetime.fromisoformat(last_change).strftime("%d/%m/%Y %H:%M:%S")
            except:
                pass
        
        # Información adicional sobre la fuente de imágenes
        if self.changer.config["mode"] == "time":
            if self.changer.config.get("use_folder", False):
                images_count = len(self.changer.get_images_from_folder())
                source = f"Carpeta ({images_count} imágenes)"
            else:
                images_count = len(self.changer.config["wallpapers"])
                source = f"Lista manual ({images_count} imágenes)"
            status_text = f"Modo actual: {mode}\nFuente: {source}\nÚltimo cambio: {last_change}"
        else:
            status_text = f"Modo actual: {mode}\nÚltimo cambio: {last_change}"
        
        self.status_label.config(text=status_text)
    
    def enable_startup(self):
        """Habilita el inicio automático"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Obtener la ruta del ejecutable o script
            if getattr(sys, 'frozen', False):
                # Si está compilado como .exe
                app_path = sys.executable
            else:
                # Si se ejecuta como script
                app_path = f'pythonw.exe "{os.path.abspath(__file__)}"'
            
            winreg.SetValueEx(key, "WallpaperChanger", 0, winreg.REG_SZ, app_path)
            winreg.CloseKey(key)
            
            self.update_startup_status()
            messagebox.showinfo("Éxito", "Inicio automático habilitado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo habilitar el inicio automático:\n{e}")
    
    def disable_startup(self):
        """Deshabilita el inicio automático"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            try:
                winreg.DeleteValue(key, "WallpaperChanger")
            except FileNotFoundError:
                pass
            
            winreg.CloseKey(key)
            
            self.update_startup_status()
            messagebox.showinfo("Éxito", "Inicio automático deshabilitado correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo deshabilitar el inicio automático:\n{e}")
    
    def update_startup_status(self):
        """Actualiza el estado del inicio automático"""
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_READ
            )
            
            try:
                winreg.QueryValueEx(key, "WallpaperChanger")
                status = "✓ Inicio automático HABILITADO"
                color = "green"
            except FileNotFoundError:
                status = "✗ Inicio automático DESHABILITADO"
                color = "red"
            
            winreg.CloseKey(key)
            
            self.startup_status_label.config(text=status, foreground=color)
        except Exception as e:
            self.startup_status_label.config(text=f"Error: {e}", foreground="orange")
    
    def create_tray_image(self):
        """Crea un icono simple para el system tray"""
        # Crear una imagen simple de 64x64
        image = PILImage.new('RGB', (64, 64), color='#2196F3')
        return image
    
    def setup_tray_icon(self):
        """Configura el icono en la bandeja del sistema"""
        image = self.create_tray_image()
        
        menu = pystray.Menu(
            pystray.MenuItem("Abrir", self.show_window, default=True),
            pystray.MenuItem("Cambiar Fondo Ahora", self.change_now_from_tray),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Salir", self.quit_app)
        )
        
        self.tray_icon = pystray.Icon(
            "WallpaperChanger",
            image,
            "Cambiador de Fondo",
            menu
        )
        
        # Iniciar el icono en un thread separado
        threading.Thread(target=self.tray_icon.run, daemon=True).start()
    
    def show_window(self, icon=None, item=None):
        """Muestra la ventana principal"""
        self.root.after(0, self._show_window)
    
    def _show_window(self):
        """Método auxiliar para mostrar ventana en el thread principal"""
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
    
    def hide_window(self):
        """Oculta la ventana principal"""
        self.root.withdraw()
    
    def change_now_from_tray(self, icon=None, item=None):
        """Cambia el fondo desde el system tray"""
        if self.changer.config["mode"] == "weekday":
            return  # No hacer nada en modo días
        
        if self.changer.change_wallpaper():
            self.tray_icon.notify(
                "Fondo Cambiado",
                "El fondo de pantalla se cambió correctamente"
            )
    
    def quit_app(self, icon=None, item=None):
        """Cierra completamente la aplicación"""
        self.changer.stop_monitoring()
        if self.tray_icon:
            self.tray_icon.stop()
        self.root.after(0, self.root.destroy)
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        # Minimizar a la bandeja en lugar de cerrar
        self.hide_window()


def main():
    root = tk.Tk()
    app = WallpaperChangerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
