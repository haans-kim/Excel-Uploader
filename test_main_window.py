"""Test MainWindow import"""
import sys
import traceback

print("Step 1: Importing customtkinter...")
import customtkinter as ctk
print("  OK")

print("Step 2: Setting appearance mode...")
ctk.set_appearance_mode("dark")
print("  OK")

print("Step 3: Importing ui.styles...")
try:
    from ui.styles import Colors, Styles
    print("  OK")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Step 4: Importing ui.main_window...")
try:
    from ui.main_window import MainWindow
    print("  OK")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Step 5: Creating MainWindow instance...")
try:
    app = MainWindow()
    print("  OK")
except Exception as e:
    print(f"  ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

print("Step 6: Starting mainloop...")
app.mainloop()
