# Hook manual para pystray
import os
import sys

# Agregar la ruta de pystray manualmente
pystray_path = r"C:\Users\USUARIO\AppData\Roaming\Python\Python314\site-packages"

if os.path.exists(pystray_path):
    datas = [(os.path.join(pystray_path, 'pystray'), 'pystray')]
    hiddenimports = ['pystray', 'pystray._win32', 'pystray._util', 'pystray._util.win32', 'six']
else:
    datas = []
    hiddenimports = []
