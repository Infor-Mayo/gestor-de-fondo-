# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Recolectar todo de pystray
pystray_datas, pystray_binaries, pystray_hiddenimports = collect_all('pystray')
ctk_datas, ctk_binaries, ctk_hiddenimports = collect_all('customtkinter')
dd_datas, dd_binaries, dd_hiddenimports = collect_all('darkdetect')

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=pystray_binaries + ctk_binaries + dd_binaries,
    datas=[('assets', 'assets')] + pystray_datas + ctk_datas + dd_datas,
    hiddenimports=['PIL._tkinter_finder', 'PIL.Image', 'PIL.ImageTk'] + pystray_hiddenimports + ctk_hiddenimports + dd_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='CambiadorDeFondo',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='CambiadorDeFondo',
)
