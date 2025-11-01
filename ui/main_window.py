"""
Main Window for SQLite Manager
"""
import customtkinter as ctk
from pathlib import Path
from ui.styles import Colors, Styles


class MainWindow(ctk.CTk):
    """Main application window"""

    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("SQLite Manager")
        self.geometry("1400x900")

        # Set color theme
        ctk.set_appearance_mode("dark")

        # Current database
        self.current_db_path = None

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI layout"""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar
        self.sidebar = self.create_sidebar()
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Create main content area
        self.main_content = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Welcome message (placeholder)
        self.create_welcome_screen()

    def create_sidebar(self):
        """Create the sidebar with navigation buttons"""
        sidebar = ctk.CTkFrame(
            self,
            width=Styles.SIDEBAR_WIDTH,
            corner_radius=0,
            fg_color=Colors.BG_SECONDARY
        )

        # Top section with title and theme toggle
        top_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        top_frame.pack(fill="x", padx=Styles.PADDING, pady=(40, 10))

        # Logo/Title
        title = ctk.CTkLabel(
            top_frame,
            text="SQLite\nManager",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack()

        # Theme toggle button
        self.theme_mode = "dark"
        self.theme_btn = ctk.CTkButton(
            sidebar,
            text="☀ Light Mode",
            width=160,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.toggle_theme
        )
        self.theme_btn.pack(padx=Styles.PADDING, pady=(0, 20))

        # Separator
        separator = ctk.CTkFrame(
            sidebar,
            height=1,
            fg_color=Colors.BORDER
        )
        separator.pack(fill="x", padx=Styles.PADDING, pady=(0, 20))

        # Section: Database
        section_label = ctk.CTkLabel(
            sidebar,
            text="DATABASE",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XS, "bold"),
            text_color=Colors.TEXT_MUTED
        )
        section_label.pack(padx=Styles.PADDING, pady=(0, 10), anchor="w")

        # Navigation buttons
        buttons = [
            ("Open Database", self.open_database),
            ("New Database", self.create_database),
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=Styles.BUTTON_HEIGHT,
                corner_radius=Styles.CORNER_RADIUS,
                fg_color=Colors.BG_TERTIARY,
                hover_color=Colors.BORDER,
                text_color=Colors.TEXT_PRIMARY,
                anchor="w",
                font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE)
            )
            btn.pack(padx=Styles.PADDING, pady=5, fill="x")

        # Section: Actions
        section_label2 = ctk.CTkLabel(
            sidebar,
            text="ACTIONS",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XS, "bold"),
            text_color=Colors.TEXT_MUTED
        )
        section_label2.pack(padx=Styles.PADDING, pady=(20, 10), anchor="w")

        action_buttons = [
            ("Upload Excel", self.upload_excel),
            ("Create Table", self.create_table_ui),
            ("Browse Tables", self.browse_tables),
        ]

        for text, command in action_buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=Styles.BUTTON_HEIGHT,
                corner_radius=Styles.CORNER_RADIUS,
                fg_color=Colors.BG_TERTIARY,
                hover_color=Colors.BORDER,
                text_color=Colors.TEXT_PRIMARY,
                anchor="w",
                font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE)
            )
            btn.pack(padx=Styles.PADDING, pady=5, fill="x")

        return sidebar

    def create_welcome_screen(self):
        """Create welcome/empty state screen"""
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Welcome card
        welcome_card = ctk.CTkFrame(
            self.main_content,
            corner_radius=Styles.CORNER_RADIUS_LG,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )
        welcome_card.pack(expand=True, fill="both")

        # Center content
        center_frame = ctk.CTkFrame(welcome_card, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Icon/Title
        title = ctk.CTkLabel(
            center_frame,
            text="DB",
            font=(Styles.FONT_FAMILY, 64, "bold"),
            text_color=Colors.ACCENT
        )
        title.pack(pady=(0, 20))

        subtitle = ctk.CTkLabel(
            center_frame,
            text="SQLite Manager",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_2XL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        subtitle.pack(pady=(0, 10))

        description = ctk.CTkLabel(
            center_frame,
            text="Manage SQLite databases and upload Excel files\nwith a clean, modern interface",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            text_color=Colors.TEXT_SECONDARY,
            justify="center"
        )
        description.pack(pady=(0, 30))

        # Action buttons
        button_frame = ctk.CTkFrame(center_frame, fg_color="transparent")
        button_frame.pack()

        open_btn = ctk.CTkButton(
            button_frame,
            text="Open Database",
            command=self.open_database,
            height=Styles.BUTTON_HEIGHT_LG,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold"),
            width=150
        )
        open_btn.pack(side="left", padx=5)

        new_btn = ctk.CTkButton(
            button_frame,
            text="New Database",
            command=self.create_database,
            height=Styles.BUTTON_HEIGHT_LG,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            width=150
        )
        new_btn.pack(side="left", padx=5)

    def open_database(self):
        """Open existing database"""
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[
                ("SQLite Database", "*.db"),
                ("SQLite Database", "*.sqlite"),
                ("SQLite Database", "*.sqlite3"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.load_database(filename)

    def create_database(self):
        """Create new database"""
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            title="Create New Database",
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")]
        )

        if filename:
            # Create empty database file
            Path(filename).touch()
            self.load_database(filename)

    def load_database(self, db_path):
        """Load database and show table list"""
        self.current_db_path = db_path
        self.title(f"SQLite Manager - {Path(db_path).name}")

        # Show database info and table list
        self.show_database_view(db_path)

    def show_database_view(self, db_path):
        """Show database information and tables"""
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Import components
        from ui.components.database_selector import DatabaseSelector
        from ui.components.table_list import TableList

        # Database info card
        self.db_selector = DatabaseSelector(self.main_content)
        self.db_selector.pack(fill="x", pady=(0, 20))
        self.db_selector.load_database(db_path)

        # Table list
        self.table_list = TableList(
            self.main_content,
            on_table_selected_callback=self.on_table_selected
        )
        self.table_list.pack(fill="both", expand=True)
        self.table_list.load_tables(db_path)

    def on_table_selected(self, table_name):
        """Handle table selection from table list"""
        self.show_table_browser(table_name)

    def show_table_browser(self, table_name):
        """Show table browser view"""
        # Clear main content
        for widget in self.main_content.winfo_children():
            widget.destroy()

        # Import component
        from ui.components.table_browser import TableBrowser

        # Create browser
        browser = TableBrowser(self.main_content, self.current_db_path, table_name)
        browser.pack(fill="both", expand=True)

        # Set back button callback
        browser.on_back = lambda: self.show_database_view(self.current_db_path)

    def upload_excel(self):
        """Upload Excel file"""
        if not self.current_db_path:
            self.show_error("Please open or create a database first")
            return

        # Open Excel uploader dialog
        from ui.components.excel_uploader import ExcelUploader

        uploader = ExcelUploader(
            self,
            self.current_db_path,
            on_complete_callback=self.on_upload_complete
        )

    def on_upload_complete(self):
        """Handle upload completion"""
        # Refresh the database view
        if self.current_db_path:
            self.show_database_view(self.current_db_path)

    def create_table_ui(self):
        """Open table creation dialog"""
        if not self.current_db_path:
            self.show_error("Please open or create a database first")
            return

        from ui.components.table_creator import TableCreator

        creator = TableCreator(
            self,
            self.current_db_path,
            on_complete_callback=self.on_table_created
        )

    def on_table_created(self):
        """Handle table creation completion"""
        # Refresh the database view
        if self.current_db_path:
            self.show_database_view(self.current_db_path)

    def toggle_theme(self):
        """Toggle between dark and light mode"""
        if self.theme_mode == "dark":
            # Switch to light mode
            self.theme_mode = "light"
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="🌙 Dark Mode")
        else:
            # Switch to dark mode
            self.theme_mode = "dark"
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="☀ Light Mode")

    def browse_tables(self):
        """Browse database tables"""
        if not self.current_db_path:
            self.show_error("Please open or create a database first")
            return

        # Show database view (which includes table list)
        self.show_database_view(self.current_db_path)

    def show_error(self, message):
        """Show error message (simple for now)"""
        from tkinter import messagebox
        messagebox.showerror("Error", message)

    def show_info(self, message):
        """Show info message (simple for now)"""
        from tkinter import messagebox
        messagebox.showinfo("Info", message)
