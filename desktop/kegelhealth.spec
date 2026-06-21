# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for Kegel Health desktop app."""

from pathlib import Path

ROOT = Path(SPECPATH).resolve().parent
ICON = ROOT / "desktop" / "assets" / "kegel.ico"

a = Analysis(
    [str(ROOT / "desktop" / "launcher.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[
        (str(ROOT / "application"), "application"),
        (str(ROOT / "data"), "data"),
        (str(ROOT / "ResearchDoc.md"), "."),
    ],
    hiddenimports=[
        "application",
        "application.create_app",
        "webview",
    ],
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
    name="KegelHealth",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ICON) if ICON.is_file() else None,
)
