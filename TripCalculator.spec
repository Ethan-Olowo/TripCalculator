# -*- mode: python ; coding: utf-8 -*-

import sys


is_macos = sys.platform == 'darwin'
is_windows = sys.platform.startswith('win')
icon_file = 'icons/AppIcon.icns' if is_macos else ('icons/AppIcon.ico' if is_windows else None)


a = Analysis(
    ['TripCalc.py'],
    pathex=[],
    binaries=[],
    datas=[('Activities.txt', '.')],
    hiddenimports=[],
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
    [],
    exclude_binaries=True,
    name='TripCalculator',
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
    icon=icon_file,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TripCalculator',
)
if is_macos:
    app = BUNDLE(
        coll,
        name='TripCalculator.app',
        icon='icons/AppIcon.icns',
        bundle_identifier=None,
    )
