"""Simple test to check CustomTkinter"""
import customtkinter as ctk

print("Creating window...")
app = ctk.CTk()
app.title("Test")
app.geometry("400x300")

label = ctk.CTkLabel(app, text="Hello World")
label.pack(pady=20)

print("Starting mainloop...")
app.mainloop()
