#!/usr/bin/env python3
"""
SQLite Manager - Main Entry Point

A modern SQLite database manager with Excel upload capabilities.
Built with CustomTkinter for a clean, shadcn/ui inspired interface.
"""
import customtkinter as ctk
from ui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Set appearance mode to dark
    ctk.set_appearance_mode("dark")

    # Set default color theme
    ctk.set_default_color_theme("blue")

    # Create and run the application
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
