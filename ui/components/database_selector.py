"""
Database Selector Component
Shows current database information and recent databases
"""
import customtkinter as ctk
from pathlib import Path
import json
from ui.styles import Colors, Styles


class DatabaseSelector(ctk.CTkFrame):
    """Database information card with quick actions"""

    def __init__(self, parent, on_db_selected_callback=None):
        super().__init__(
            parent,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )

        self.on_db_selected = on_db_selected_callback
        self.current_db_path = None

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components"""
        # Header with DB icon and name
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=Styles.PADDING, pady=(Styles.PADDING, 10))

        self.db_icon = ctk.CTkLabel(
            header_frame,
            text="DB",
            font=(Styles.FONT_FAMILY, 24, "bold"),
            text_color=Colors.ACCENT
        )
        self.db_icon.pack(side="left", padx=(0, 10))

        info_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="x", expand=True)

        self.db_name_label = ctk.CTkLabel(
            info_frame,
            text="No Database Selected",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
            text_color=Colors.TEXT_PRIMARY,
            anchor="w"
        )
        self.db_name_label.pack(fill="x")

        self.db_path_label = ctk.CTkLabel(
            info_frame,
            text="Open or create a database to get started",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY,
            anchor="w"
        )
        self.db_path_label.pack(fill="x")

        # Stats row
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=Styles.PADDING, pady=(0, Styles.PADDING))

        self.size_label = ctk.CTkLabel(
            self.stats_frame,
            text="",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_MUTED
        )
        self.size_label.pack(side="left", padx=(0, 20))

        self.tables_label = ctk.CTkLabel(
            self.stats_frame,
            text="",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_MUTED
        )
        self.tables_label.pack(side="left")

    def load_database(self, db_path):
        """Load and display database information"""
        self.current_db_path = db_path
        db_file = Path(db_path)

        # Update DB name
        self.db_name_label.configure(text=db_file.name)
        self.db_path_label.configure(text=str(db_path))

        # Get file size
        size_bytes = db_file.stat().st_size
        if size_bytes < 1024:
            size_str = f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            size_str = f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            size_str = f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"

        self.size_label.configure(text=f"Size: {size_str}")

        # Get table count
        from core.db_manager import DatabaseManager
        try:
            db = DatabaseManager(db_path)
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            table_count = cursor.fetchone()[0]
            self.tables_label.configure(text=f"Tables: {table_count}")
        except Exception as e:
            self.tables_label.configure(text=f"Error: {str(e)[:30]}")

        # Save to recent databases
        self.save_recent_database(db_path)

    def save_recent_database(self, db_path):
        """Save database to recent list"""
        config_dir = Path(__file__).parent.parent.parent / "config"
        config_dir.mkdir(exist_ok=True)
        recent_file = config_dir / "recent_dbs.json"

        # Load existing
        if recent_file.exists():
            with open(recent_file, 'r') as f:
                recent = json.load(f)
        else:
            recent = []

        # Add new (remove duplicates)
        db_path = str(Path(db_path).absolute())
        if db_path in recent:
            recent.remove(db_path)
        recent.insert(0, db_path)

        # Keep only last 10
        recent = recent[:10]

        # Save
        with open(recent_file, 'w') as f:
            json.dump(recent, f, indent=2)
