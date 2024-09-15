# -*- mode: python ; coding: utf-8 -*-

import os,sys
from PyInstaller.utils.hooks import collect_data_files

base_path = os.getenv('BASE_PATH',  os.path.dirname(sys.argv[0]))

a = Analysis(
    [os.path.join(base_path, 'main.py')],
    pathex=[],
    binaries=[],
    datas=[(os.path.join(base_path, 'siui'), 'siui'), (os.path.join(base_path, 'uiprofile\\icon'), 'uiprofile\\icon'), (os.path.join(base_path, 'uiprofile'), 'uiprofile'),(os.path.join(base_path, 'main.py'), '.')],
    hiddenimports=['numpy', 'PyQt5.QtSvg', 'pyperclip', 'PyQt5.Qt', 'SDK'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='awtools',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    icon = os.path.join(base_path,'icon.ico'),
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
