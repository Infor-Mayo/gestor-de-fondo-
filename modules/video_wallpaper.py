"""
Módulo para manejar videos como fondos de pantalla
Utiliza Windows API para establecer videos como fondo animado
"""

import os
import ctypes
import subprocess
import threading
import time
from pathlib import Path
from typing import Optional, List
import winreg


class VideoWallpaperEngine:
    """Motor para establecer videos como fondos de pantalla en Windows"""
    
    def __init__(self):
        """Inicializa el motor de videos"""
        self.current_video_process = None
        self.is_video_playing = False
        self.video_thread = None
        
    def is_video_file(self, file_path: str) -> bool:
        """
        Verifica si un archivo es un video soportado
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            True si es un video soportado
        """
        video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        return Path(file_path).suffix.lower() in video_extensions
    
    def get_videos_from_folder(self, folder_path: str) -> List[str]:
        """
        Obtiene todos los videos de una carpeta
        
        Args:
            folder_path: Ruta de la carpeta
            
        Returns:
            Lista de rutas de videos
        """
        if not os.path.exists(folder_path):
            return []
        
        videos = []
        video_extensions = {'.mp4', '.avi', '.mov', '.wmv', '.mkv', '.flv', '.webm', '.m4v'}
        
        try:
            for file in os.listdir(folder_path):
                if Path(file).suffix.lower() in video_extensions:
                    full_path = os.path.join(folder_path, file)
                    videos.append(full_path)
        except Exception as e:
            print(f"Error leyendo videos de carpeta: {e}")
        
        return sorted(videos)
    
    def set_video_wallpaper(self, video_path: str) -> bool:
        """
        Establece un video como fondo de pantalla (versión simplificada)
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se estableció correctamente
        """
        try:
            # Detener video anterior si existe
            self.stop_video_wallpaper()
            
            if not os.path.exists(video_path):
                print(f"❌ El archivo de video no existe: {video_path}")
                return False
            
            # Verificar que es un video
            if not self.is_video_file(video_path):
                print(f"❌ El archivo no es un video soportado: {video_path}")
                return False
            
            print(f"🎬 Estableciendo video como fondo: {os.path.basename(video_path)}")
            
            # Usar método simple: extraer frame del video como imagen
            success = self._set_video_frame_as_wallpaper(video_path)
            
            if success:
                self.is_video_playing = True
                print(f"✅ Video establecido como fondo (frame estático): {os.path.basename(video_path)}")
                return True
            else:
                print(f"⚠️ Falló extracción de frame, usando placeholder...")
                # Fallback: crear imagen placeholder
                return self._create_video_thumbnail_wallpaper(video_path)
                
        except Exception as e:
            print(f"❌ Error estableciendo video como fondo: {e}")
            return False
    
    def _start_animated_video_wallpaper(self, video_path: str) -> bool:
        """
        Inicia reproducción de video animado usando ventana transparente
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se inició correctamente
        """
        try:
            import threading
            import tkinter as tk
            import cv2
            from PIL import Image, ImageTk
            import time
            
            # Detener video anterior
            self.stop_video_wallpaper()
            
            # Crear ventana para video
            def create_video_window():
                try:
                    # Crear ventana de video
                    self.video_window = tk.Toplevel()
                    self.video_window.title("Video Wallpaper")
                    
                    # Configurar ventana para que esté detrás de todo
                    self.video_window.attributes('-topmost', False)
                    self.video_window.attributes('-alpha', 1.0)
                    self.video_window.overrideredirect(True)  # Sin bordes
                    
                    # Obtener tamaño de pantalla
                    screen_width = self.video_window.winfo_screenwidth()
                    screen_height = self.video_window.winfo_screenheight()
                    
                    # Configurar ventana a pantalla completa
                    self.video_window.geometry(f"{screen_width}x{screen_height}+0+0")
                    self.video_window.configure(bg='black')
                    
                    # Crear label para mostrar video
                    self.video_label = tk.Label(self.video_window, bg='black')
                    self.video_label.pack(fill='both', expand=True)
                    
                    # Enviar ventana al fondo
                    self._send_window_to_back()
                    
                    print("✅ Ventana de video creada")
                    return True
                    
                except Exception as e:
                    print(f"❌ Error creando ventana de video: {e}")
                    return False
            
            # Crear ventana en el hilo principal
            if not create_video_window():
                return False
            
            # Iniciar reproducción en hilo separado
            def play_video():
                try:
                    cap = cv2.VideoCapture(video_path)
                    
                    if not cap.isOpened():
                        print(f"❌ No se pudo abrir video: {video_path}")
                        return
                    
                    # Obtener propiedades del video
                    fps = cap.get(cv2.CAP_PROP_FPS) or 30
                    frame_delay = 1.0 / fps
                    
                    print(f"🎬 Reproduciendo video a {fps} FPS")
                    
                    while self.is_video_playing and hasattr(self, 'video_window'):
                        ret, frame = cap.read()
                        
                        if not ret:
                            # Reiniciar video (loop)
                            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                            continue
                        
                        try:
                            # Convertir frame de BGR a RGB
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            
                            # Redimensionar frame al tamaño de pantalla
                            screen_width = self.video_window.winfo_screenwidth()
                            screen_height = self.video_window.winfo_screenheight()
                            
                            # Crear imagen PIL
                            pil_image = Image.fromarray(frame_rgb)
                            pil_image = pil_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
                            
                            # Convertir a PhotoImage
                            photo = ImageTk.PhotoImage(pil_image)
                            
                            # Actualizar label en el hilo principal usando after()
                            if hasattr(self, 'video_label') and self.video_label.winfo_exists():
                                def update_frame():
                                    try:
                                        if hasattr(self, 'video_label') and self.video_label.winfo_exists():
                                            self.video_label.configure(image=photo)
                                            self.video_label.image = photo  # Mantener referencia
                                    except:
                                        pass
                                
                                # Programar actualización en el hilo principal
                                self.video_window.after(0, update_frame)
                            
                        except Exception as e:
                            print(f"⚠️ Error procesando frame: {e}")
                        
                        # Esperar según FPS
                        time.sleep(frame_delay)
                    
                    cap.release()
                    print("🛑 Reproducción de video terminada")
                    
                except Exception as e:
                    print(f"❌ Error en reproducción de video: {e}")
            
            # Iniciar hilo de reproducción
            self.video_thread = threading.Thread(target=play_video, daemon=True)
            self.video_thread.start()
            
            return True
            
        except ImportError as e:
            print(f"❌ Dependencias no disponibles para video animado: {e}")
            return False
        except Exception as e:
            print(f"❌ Error iniciando video animado: {e}")
            return False
    
    def _send_window_to_back(self):
        """Envía la ventana de video al fondo (detrás de todas las ventanas)"""
        try:
            import ctypes
            from ctypes import wintypes
            
            # Obtener handle de la ventana
            hwnd = self.video_window.winfo_id()
            
            # Constantes de Windows
            HWND_BOTTOM = 1
            SWP_NOSIZE = 0x0001
            SWP_NOMOVE = 0x0002
            SWP_NOACTIVATE = 0x0010
            
            # Enviar ventana al fondo
            ctypes.windll.user32.SetWindowPos(
                hwnd, HWND_BOTTOM, 0, 0, 0, 0,
                SWP_NOSIZE | SWP_NOMOVE | SWP_NOACTIVATE
            )
            
            print("✅ Ventana enviada al fondo")
            
        except Exception as e:
            print(f"⚠️ No se pudo enviar ventana al fondo: {e}")
    
    def _set_video_frame_as_wallpaper(self, video_path: str) -> bool:
        """
        Extrae el primer frame del video y lo usa como fondo de pantalla
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se estableció correctamente
        """
        try:
            import cv2
            import tempfile
            import ctypes
            
            # Abrir video con OpenCV
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"❌ No se pudo abrir el video con OpenCV")
                return False
            
            # Leer primer frame
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                print(f"❌ No se pudo leer frame del video")
                return False
            
            # Guardar frame como imagen temporal
            temp_dir = tempfile.gettempdir()
            temp_image = os.path.join(temp_dir, "video_wallpaper_frame.jpg")
            
            # Guardar frame
            cv2.imwrite(temp_image, frame)
            
            # Establecer como fondo de pantalla usando Windows API
            SPI_SETDESKWALLPAPER = 20
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                temp_image, 
                3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            
            if result:
                print(f"✅ Frame del video establecido como fondo")
                return True
            else:
                print(f"❌ Error estableciendo frame como fondo")
                return False
                
        except ImportError:
            print(f"❌ OpenCV no disponible para procesar video")
            return False
        except Exception as e:
            print(f"❌ Error procesando frame del video: {e}")
            return False
    
    def _create_video_thumbnail_wallpaper(self, video_path: str) -> bool:
        """
        Crea una imagen thumbnail del video y la usa como fondo
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se estableció correctamente
        """
        try:
            import tempfile
            import ctypes
            from PIL import Image, ImageDraw, ImageFont
            
            # Crear imagen con información del video
            img_width, img_height = 1920, 1080
            img = Image.new('RGB', (img_width, img_height), color='black')
            draw = ImageDraw.Draw(img)
            
            # Agregar texto con información del video
            video_name = os.path.basename(video_path)
            
            try:
                # Intentar usar fuente del sistema
                font_large = ImageFont.truetype("arial.ttf", 48)
                font_small = ImageFont.truetype("arial.ttf", 24)
            except:
                # Usar fuente por defecto si no encuentra arial
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Texto principal
            text1 = "🎬 VIDEO WALLPAPER"
            text2 = f"📁 {video_name}"
            text3 = "⚠️ Reproducción de video no disponible"
            text4 = "💡 Mostrando imagen estática del video"
            
            # Centrar textos
            y_pos = img_height // 2 - 100
            
            # Dibujar textos
            bbox1 = draw.textbbox((0, 0), text1, font=font_large)
            x1 = (img_width - (bbox1[2] - bbox1[0])) // 2
            draw.text((x1, y_pos), text1, fill='white', font=font_large)
            
            bbox2 = draw.textbbox((0, 0), text2, font=font_small)
            x2 = (img_width - (bbox2[2] - bbox2[0])) // 2
            draw.text((x2, y_pos + 60), text2, fill='lightblue', font=font_small)
            
            bbox3 = draw.textbbox((0, 0), text3, font=font_small)
            x3 = (img_width - (bbox3[2] - bbox3[0])) // 2
            draw.text((x3, y_pos + 120), text3, fill='orange', font=font_small)
            
            bbox4 = draw.textbbox((0, 0), text4, font=font_small)
            x4 = (img_width - (bbox4[2] - bbox4[0])) // 2
            draw.text((x4, y_pos + 150), text4, fill='gray', font=font_small)
            
            # Guardar imagen temporal
            temp_dir = tempfile.gettempdir()
            temp_image = os.path.join(temp_dir, "video_wallpaper_placeholder.jpg")
            img.save(temp_image, "JPEG", quality=95)
            
            # Establecer como fondo de pantalla
            SPI_SETDESKWALLPAPER = 20
            result = ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                temp_image, 
                3  # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
            
            if result:
                print(f"✅ Imagen placeholder del video establecida como fondo")
                return True
            else:
                print(f"❌ Error estableciendo placeholder como fondo")
                return False
                
        except Exception as e:
            print(f"❌ Error creando thumbnail del video: {e}")
            return False
    
    def _set_video_as_wallpaper_wmp(self, video_path: str) -> bool:
        """
        Método usando Windows Media Player para video como fondo
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se estableció correctamente
        """
        try:
            # Crear archivo HTML que reproduce el video en bucle
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{ margin: 0; padding: 0; overflow: hidden; }}
                    video {{ width: 100vw; height: 100vh; object-fit: cover; }}
                </style>
            </head>
            <body>
                <video autoplay muted loop>
                    <source src="file:///{video_path.replace(os.sep, '/')}" type="video/mp4">
                </video>
            </body>
            </html>
            """
            
            # Guardar HTML temporal
            temp_html = os.path.join(os.path.dirname(video_path), "video_wallpaper.html")
            with open(temp_html, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Usar PowerShell para establecer como fondo activo
            powershell_script = f"""
            Add-Type -TypeDefinition @"
                using System;
                using System.Runtime.InteropServices;
                public class Wallpaper {{
                    [DllImport("user32.dll", CharSet=CharSet.Auto)]
                    public static extern int SystemParametersInfo(int uAction, int uParam, string lpvParam, int fuWinIni);
                }}
"@
            [Wallpaper]::SystemParametersInfo(20, 0, "{temp_html}", 3)
            """
            
            # Ejecutar PowerShell
            result = subprocess.run([
                "powershell", "-Command", powershell_script
            ], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
            
            return result.returncode == 0
            
        except Exception as e:
            print(f"Error en método WMP: {e}")
            return False
    
    def _set_video_as_wallpaper_alternative(self, video_path: str) -> bool:
        """
        Método alternativo usando reproductores externos
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se estableció correctamente
        """
        try:
            # Intentar con VLC en modo wallpaper
            vlc_paths = [
                r"C:\Program Files\VideoLAN\VLC\vlc.exe",
                r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"
            ]
            
            for vlc_path in vlc_paths:
                if os.path.exists(vlc_path):
                    # Ejecutar VLC en modo wallpaper
                    cmd = [
                        vlc_path,
                        video_path,
                        "--intf", "dummy",
                        "--loop",
                        "--no-video-title-show",
                        "--video-wallpaper"
                    ]
                    
                    self.current_video_process = subprocess.Popen(
                        cmd, 
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    
                    time.sleep(2)  # Esperar a que inicie
                    
                    if self.current_video_process.poll() is None:
                        return True
            
            # Si VLC no está disponible, usar método de ventana transparente
            return self._create_transparent_video_window(video_path)
            
        except Exception as e:
            print(f"Error en método alternativo: {e}")
            return False
    
    def _create_transparent_video_window(self, video_path: str) -> bool:
        """
        Crea una ventana transparente que reproduce el video como fondo
        
        Args:
            video_path: Ruta del video
            
        Returns:
            True si se creó correctamente
        """
        try:
            # Crear script Python para ventana de video
            script_content = f"""
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import threading
import time

class VideoWallpaper:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', False)
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        
        # Enviar ventana al fondo
        self.root.lower()
        
        self.label = tk.Label(self.root, bg='black')
        self.label.pack(fill=tk.BOTH, expand=True)
        
        self.cap = cv2.VideoCapture(r"{video_path}")
        self.playing = True
        
        self.play_video()
        self.root.mainloop()
    
    def play_video(self):
        def video_loop():
            while self.playing:
                ret, frame = self.cap.read()
                if not ret:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reiniciar video
                    continue
                
                # Redimensionar frame
                height = self.root.winfo_screenheight()
                width = self.root.winfo_screenwidth()
                frame = cv2.resize(frame, (width, height))
                
                # Convertir a formato Tkinter
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                photo = ImageTk.PhotoImage(img)
                
                # Actualizar label
                self.label.configure(image=photo)
                self.label.image = photo
                
                time.sleep(0.033)  # ~30 FPS
        
        thread = threading.Thread(target=video_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    VideoWallpaper()
"""
            
            # Guardar script temporal
            script_path = os.path.join(os.path.dirname(video_path), "video_wallpaper_player.py")
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Ejecutar script
            self.current_video_process = subprocess.Popen([
                "python", script_path
            ], creationflags=subprocess.CREATE_NO_WINDOW)
            
            return True
            
        except Exception as e:
            print(f"Error creando ventana de video: {e}")
            return False
    
    def stop_video_wallpaper(self) -> bool:
        """
        Detiene el video de fondo actual
        
        Returns:
            True si se detuvo correctamente
        """
        try:
            print("🛑 Deteniendo reproducción de video...")
            
            # Detener reproducción
            self.is_video_playing = False
            
            # Cerrar ventana de video si existe
            if hasattr(self, 'video_window') and self.video_window:
                try:
                    self.video_window.destroy()
                    delattr(self, 'video_window')
                    print("✅ Ventana de video cerrada")
                except:
                    pass
            
            # Detener hilo de video si existe
            if hasattr(self, 'video_thread') and self.video_thread:
                try:
                    # El hilo se detendrá automáticamente cuando is_video_playing sea False
                    self.video_thread = None
                    print("✅ Hilo de video detenido")
                except:
                    pass
            
            # Detener proceso de video si existe (método antiguo)
            if self.current_video_process:
                try:
                    # Solicitar terminación y esperar un breve tiempo
                    self.current_video_process.terminate()
                    try:
                        self.current_video_process.wait(timeout=2)
                    except Exception:
                        pass
                    # Si sigue vivo, forzar cierre
                    if self.current_video_process.poll() is None:
                        try:
                            self.current_video_process.kill()
                        except Exception:
                            pass
                    print("✅ Proceso de video terminado")
                except Exception:
                    pass
                finally:
                    self.current_video_process = None
            
            # Restaurar fondo sólido
            self._restore_default_wallpaper()
            
            print("✅ Video de fondo detenido completamente")
            return True
            
        except Exception as e:
            print(f"Error deteniendo video: {e}")
            return False
    
    def _restore_default_wallpaper(self):
        """Restaura el fondo de pantalla por defecto"""
        try:
            # Establecer color sólido negro como fondo
            SPI_SETDESKWALLPAPER = 20
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 
                0, 
                "", 
                3
            )
        except Exception as e:
            print(f"Error restaurando fondo: {e}")
    
    def is_playing(self) -> bool:
        """
        Verifica si hay un video reproduciéndose
        
        Returns:
            True si hay un video activo
        """
        return self.is_video_playing and (
            self.current_video_process is None or 
            self.current_video_process.poll() is None
        )
