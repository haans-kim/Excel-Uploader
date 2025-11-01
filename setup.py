from cx_Freeze import setup, Executable
import sys

# Dependencies
build_exe_options = {
    "packages": [
        "customtkinter",
        "tkinter",
        "pandas",
        "openpyxl",
        "sqlite3",
    ],
    "include_files": [
        ("ui", "ui"),
        ("core", "core"),
    ],
    "excludes": [
        "matplotlib",
        "numpy.distutils",
        "IPython",
        "notebook",
    ],
}

# Base for Windows GUI application
base = "Win32GUI" if sys.platform == "win32" else None

setup(
    name="SQLiteManager",
    version="1.0",
    description="SQLite Manager with Excel Upload",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="SQLiteManager.exe")],
)
