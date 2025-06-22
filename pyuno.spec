# -*- mode: python ; coding: utf-8 -*-

import os
import platform
from pathlib import Path

# Get the directory containing this spec file
spec_root = Path(SPECPATH)

# Define paths
assets_path = spec_root / 'assets'
src_path = spec_root / 'src'

# Platform detection
is_windows = platform.system() == 'Windows'
is_macos = platform.system() == 'Darwin'
is_linux = platform.system() == 'Linux'

# Collect all asset files
asset_files = []
if assets_path.exists():
    for file_path in assets_path.rglob('*'):
        if file_path.is_file():
            relative_path = file_path.relative_to(spec_root)
            asset_files.append((str(file_path), str(relative_path.parent)))

# Collect all source files
src_files = []
if src_path.exists():
    for file_path in src_path.rglob('*.py'):
        if file_path.is_file():
            relative_path = file_path.relative_to(spec_root)
            src_files.append((str(file_path), str(relative_path.parent)))

# Find appropriate icon
icon_file = None
possible_icons = [
    assets_path / 'uno_logo.icns' if is_macos else None,
    assets_path / 'uno_logo.ico' if is_windows else None,
    assets_path / 'uno_logo.png'
]

for icon_path in possible_icons:
    if icon_path and icon_path.exists():
        icon_file = str(icon_path)
        break

block_cipher = None

a = Analysis(
    ['main_game.py'],
    pathex=[str(spec_root)],
    binaries=[],
    datas=asset_files + src_files,
    hiddenimports=[
        'pygame',
        'src.pyuno',
        'src.pyuno.core',
        'src.pyuno.core.uno_classes',
        'src.pyuno.ui',
        'src.pyuno.ui.uno_ui',
        'src.pyuno.config',
        'src.pyuno.config.font_config'
    ],
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PyUNO',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True if you want to see console output for debugging
    disable_windowed_traceback=False,
    target_arch='universal2' if is_macos else None,  # Support both Intel and Apple Silicon on macOS
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file
)

# macOS specific: Create .app bundle
if is_macos:
    app = BUNDLE(
        exe,
        name='PyUNO.app',
        icon=icon_file,
        bundle_identifier='com.pyuno.game',
        info_plist={
            'CFBundleName': 'PyUNO',
            'CFBundleDisplayName': 'PyUNO Card Game',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': 'True',
        }
    ) 