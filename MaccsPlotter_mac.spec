# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['new_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('images', 'images')],
    hiddenimports=['matplotlib.backends.backend_pdf'],
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
    name='MACCS Plotter',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MACCS Plotter',
)
app = BUNDLE(
    coll,
    name='MACCS Plotter.app',
    icon="images/maccslogo_nobg.icns",
    bundle_identifier=None,
)
