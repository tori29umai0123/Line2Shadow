# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files

datas = [('C:\\Line2Shadow\\javascript', '.\\javascript'), ('C:\\Line2Shadow\\ldm_patched', '.\\ldm_patched'), ('C:\\Line2Shadow\\localizations', '.\\localizations'), ('C:\\Line2Shadow\\modules', '.\\modules'), ('C:\\Line2Shadow\\modules_forge', '.\\modules_forge'), ('C:\\Line2Shadow\\repositories', '.\\repositories'), ('C:\\Line2Shadow\\cache.json', '.'), ('C:\\Line2Shadow\\script.js', '.'), ('C:\\Line2Shadow\\ui-config.json', '.'), ('C:\\Line2Shadow\\config_states', '.\\config_states'), ('C:\\Line2Shadow\\configs', '.\\configs'), ('C:\\Line2Shadow\\extensions-builtin', '.\\extensions-builtin'), ('C:\\Line2Shadow\\html', '.\\html')]
datas += collect_data_files('tkinterdnd2')


a = Analysis(
    ['C:\\Line2Shadow\\Line2Shadow.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Line2Shadow',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Line2Shadow',
)
