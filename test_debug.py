"""Debug MainWindow creation step by step"""
import customtkinter as ctk
from pathlib import Path
from ui.styles import Colors, Styles

print("Creating CTk instance...")
app = ctk.CTk()
print("  OK")

print("Setting title and geometry...")
app.title("SQLite Manager")
app.geometry("1400x900")
print("  OK")

print("Setting appearance mode...")
ctk.set_appearance_mode("dark")
print("  OK")

print("Configuring grid...")
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)
print("  OK")

print("Creating sidebar frame...")
sidebar = ctk.CTkFrame(
    app,
    width=Styles.SIDEBAR_WIDTH,
    corner_radius=0,
    fg_color=Colors.BG_SECONDARY
)
print("  OK")

print("Creating sidebar title...")
title = ctk.CTkLabel(
    sidebar,
    text="SQLite\nManager",
    font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
    text_color=Colors.TEXT_PRIMARY
)
title.pack(padx=Styles.PADDING, pady=(40, 30))
print("  OK")

print("Placing sidebar on grid...")
sidebar.grid(row=0, column=0, sticky="nsew")
print("  OK")

print("Creating main content area...")
main_content = ctk.CTkFrame(app, fg_color="transparent")
main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
print("  OK")

print("Creating test label in main content...")
test_label = ctk.CTkLabel(main_content, text="Test Content")
test_label.pack(pady=20)
print("  OK")

print("Starting mainloop...")
app.mainloop()
