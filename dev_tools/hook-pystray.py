"""
Hook personalizado para PyInstaller - pystray
"""

from PyInstaller.utils.hooks import collect_all, collect_submodules

# Recolectar todos los submódulos de pystray
datas, binaries, hiddenimports = collect_all('pystray')

# Agregar submódulos específicos
hiddenimports += collect_submodules('pystray')
hiddenimports += [
    'pystray._win32',
    'pystray._util',
    'pystray._util.win32',
    'six',
]
