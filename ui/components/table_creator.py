"""
Table Creator Component
Create new database tables with custom schema
"""
import customtkinter as ctk
from tkinter import messagebox
from ui.styles import Colors, Styles


class TableCreator(ctk.CTkToplevel):
    """Table creation dialog"""

    def __init__(self, parent, db_path, on_complete_callback=None):
        super().__init__(parent)

        self.db_path = db_path
        self.on_complete = on_complete_callback
        self.columns = []

        # Window configuration
        self.title("Create New Table")
        self.geometry("700x600")
        self.resizable(False, False)

        # Set appearance
        ctk.set_appearance_mode("dark")

        # Make modal
        self.transient(parent)
        self.grab_set()

        self.setup_ui()

    def setup_ui(self):
        """Setup the UI components"""
        # Main container
        container = ctk.CTkFrame(
            self,
            fg_color=Colors.BG_PRIMARY,
            corner_radius=0
        )
        container.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            container,
            text="Create New Table",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(pady=(0, 20))

        # Table name
        name_frame = ctk.CTkFrame(container, fg_color=Colors.BG_SECONDARY)
        name_frame.pack(fill="x", pady=(0, 20))

        name_label = ctk.CTkLabel(
            name_frame,
            text="Table Name:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            text_color=Colors.TEXT_SECONDARY
        )
        name_label.pack(padx=Styles.PADDING, pady=(Styles.PADDING, 5), anchor="w")

        self.table_name_entry = ctk.CTkEntry(
            name_frame,
            height=Styles.INPUT_HEIGHT,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE)
        )
        self.table_name_entry.pack(padx=Styles.PADDING, pady=(0, Styles.PADDING), fill="x")

        # Columns section
        columns_label = ctk.CTkLabel(
            container,
            text="Columns:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        columns_label.pack(anchor="w", pady=(0, 10))

        # Scrollable frame for columns
        self.columns_frame = ctk.CTkScrollableFrame(
            container,
            height=300,
            fg_color=Colors.BG_SECONDARY
        )
        self.columns_frame.pack(fill="both", expand=True, pady=(0, 10))

        # Add column button
        add_col_btn = ctk.CTkButton(
            container,
            text="+ Add Column",
            command=self.add_column_row,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        )
        add_col_btn.pack(pady=(0, 20))

        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x")

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=120,
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER
        )
        cancel_btn.pack(side="right", padx=(10, 0))

        create_btn = ctk.CTkButton(
            button_frame,
            text="Create Table",
            command=self.create_table,
            width=120,
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.SUCCESS,
            hover_color=Colors.SUCCESS_HOVER
        )
        create_btn.pack(side="right")

        # Add first column row
        self.add_column_row()

    def add_column_row(self):
        """Add a new column input row"""
        row_frame = ctk.CTkFrame(self.columns_frame, fg_color=Colors.BG_TERTIARY)
        row_frame.pack(fill="x", pady=5, padx=10)

        # Column name
        name_entry = ctk.CTkEntry(
            row_frame,
            placeholder_text="Column name",
            width=200,
            height=Styles.INPUT_HEIGHT_SM
        )
        name_entry.pack(side="left", padx=5, pady=5)

        # Data type
        type_var = ctk.StringVar(value="TEXT")
        type_menu = ctk.CTkOptionMenu(
            row_frame,
            variable=type_var,
            values=["TEXT", "INTEGER", "REAL", "BLOB"],
            width=100,
            height=Styles.INPUT_HEIGHT_SM
        )
        type_menu.pack(side="left", padx=5)

        # Constraints
        constraints_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        constraints_frame.pack(side="left", padx=5)

        primary_key_var = ctk.BooleanVar()
        pk_check = ctk.CTkCheckBox(
            constraints_frame,
            text="PK",
            variable=primary_key_var,
            width=50,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XS)
        )
        pk_check.pack(side="left", padx=2)

        not_null_var = ctk.BooleanVar()
        nn_check = ctk.CTkCheckBox(
            constraints_frame,
            text="NOT NULL",
            variable=not_null_var,
            width=80,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XS)
        )
        nn_check.pack(side="left", padx=2)

        unique_var = ctk.BooleanVar()
        unique_check = ctk.CTkCheckBox(
            constraints_frame,
            text="UNIQUE",
            variable=unique_var,
            width=70,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XS)
        )
        unique_check.pack(side="left", padx=2)

        # Remove button
        remove_btn = ctk.CTkButton(
            row_frame,
            text="×",
            width=30,
            height=Styles.INPUT_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.ERROR,
            hover_color=Colors.ERROR_HOVER,
            command=lambda: self.remove_column_row(row_frame)
        )
        remove_btn.pack(side="right", padx=5)

        # Store references
        self.columns.append({
            'frame': row_frame,
            'name': name_entry,
            'type': type_var,
            'pk': primary_key_var,
            'not_null': not_null_var,
            'unique': unique_var
        })

    def remove_column_row(self, frame):
        """Remove a column row"""
        # Find and remove from columns list
        self.columns = [col for col in self.columns if col['frame'] != frame]
        frame.destroy()

    def create_table(self):
        """Create the table in database"""
        # Validate table name
        table_name = self.table_name_entry.get().strip()
        if not table_name:
            messagebox.showerror("Error", "Please enter a table name")
            return

        # Validate columns
        if not self.columns:
            messagebox.showerror("Error", "Please add at least one column")
            return

        # Build CREATE TABLE statement
        columns_sql = []
        for col in self.columns:
            col_name = col['name'].get().strip()
            if not col_name:
                messagebox.showerror("Error", "All columns must have a name")
                return

            col_type = col['type'].get()
            constraints = []

            if col['pk'].get():
                constraints.append("PRIMARY KEY")
            if col['not_null'].get():
                constraints.append("NOT NULL")
            if col['unique'].get():
                constraints.append("UNIQUE")

            col_def = f"{col_name} {col_type}"
            if constraints:
                col_def += " " + " ".join(constraints)

            columns_sql.append(col_def)

        create_sql = f"CREATE TABLE {table_name} (\n    {',\n    '.join(columns_sql)}\n)"

        try:
            from core.db_manager import DatabaseManager

            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(create_sql)
            conn.commit()

            messagebox.showinfo("Success", f"Table '{table_name}' created successfully!")

            # Call completion callback
            if self.on_complete:
                self.on_complete()

            # Close dialog
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create table:\n{str(e)}")

    def cancel(self):
        """Cancel and close dialog"""
        self.destroy()
