# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Website Games Launcher
This provides more fine-grained control over the build process

To use this file instead of setup.py:
    pyinstaller WebsiteGamesLauncher.spec
"""

import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect all submodules
hiddenimports = [
    'core',
    'core.achievement_manager',
    'core.download_manager',
    'core.game_manager',
    'core.settings_manager',
    'gui',
    'gui.main_window',
    'gui.tabs',
    'gui.tabs.games_tab',
    'gui.widgets',
    'gui.widgets.fullscreen_game_window',
    'models',
    'models.achievement',
    'models.daily_challenge',
    'models.game_item',
    'utils',
    'utils.daily_challenge_generator',
    'utils.update_checker',
]

# Add PyQt5 imports (change to PyQt6 or PySide6 if needed)
hiddenimports += [
    'PyQt5',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtWebEngineWidgets',
]

# Data files to include
datas = [
    ('core', 'core'),
    ('gui', 'gui'),
    ('models', 'models'),
    ('utils', 'utils'),
    ('README.md', '.'),
    ('LICENSE', '.'),
]

# Binary files (if any)
binaries = []

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PIL',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='WebsiteGamesLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX if available
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add 'icon.ico' if you have an icon file
)
