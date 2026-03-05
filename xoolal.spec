# -*- mode: python ; coding: utf-8 -*-
# ============================================
# Xoolal Browser - Configuration PyInstaller
# © 2024 Ismaïla Mbodji
# ============================================

block_cipher = None

a = Analysis(
    ['navigateur.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('accueil.html', '.'),
        ('xoolal_icon.png', '.'),
        ('bloqueur.py', '.'),
        ('moteur.py', '.'),
        ('cookies.py', '.'),
    ],
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtWebEngineCore',
        'PyQt5.QtPrintSupport',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Xoolal',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon='xoolal_icon.png',
)

# Pour Mac — crée un .app
app = BUNDLE(
    exe,
    name='Xoolal.app',
    icon='xoolal_icon.png',
    bundle_identifier='sn.xoolal.browser',
    info_plist={
        'CFBundleName': 'Xoolal',
        'CFBundleDisplayName': 'Xoolal Browser',
        'CFBundleVersion': '1.4.0',
        'CFBundleShortVersionString': '1.4',
        'NSHighResolutionCapable': True,
        'CFBundleIdentifier': 'sn.xoolal.browser',
        'NSHumanReadableCopyright': '© 2024 Ismaïla Mbodji',
    },
)
