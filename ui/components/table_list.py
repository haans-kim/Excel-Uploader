"""
Table List Component
TreeView displaying all tables in the database
"""
import customtkinter as ctk
from tkinter import ttk
from ui.styles import Colors, Styles


class TableList(ctk.CTkFrame):
    """Table list with TreeView"""

    def __init__(self, parent, on_table_selected_callback=None):
        super().__init__(
            parent,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )

        self.on_table_selected = on_table_selected_callback
        self.db_path = None

        self.setup_ui()
        self.setup_treeview_style()

    def setup_ui(self):
        """Setup the UI components"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=Styles.PADDING, pady=(Styles.PADDING, 10))

        title = ctk.CTkLabel(
            header,
            text="Tables",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_LG, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(side="left")

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            header,
            text="↻",
            width=30,
            height=30,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.refresh_tables,
            font=(Styles.FONT_FAMILY, 16)
        )
        self.refresh_btn.pack(side="right")

        # TreeView container
        tree_container = ctk.CTkFrame(self, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=Styles.PADDING, pady=(0, Styles.PADDING))

        # Create TreeView
        self.tree = ttk.Treeview(
            tree_container,
            columns=("columns", "rows"),
            show="tree headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        # Configure columns
        self.tree.heading("#0", text="Table Name")
        self.tree.heading("columns", text="Columns")
        self.tree.heading("rows", text="Rows")

        self.tree.column("#0", width=250, minwidth=150)
        self.tree.column("columns", width=80, anchor="center")
        self.tree.column("rows", width=120, anchor="e")

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(
            tree_container,
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind double-click
        self.tree.bind("<Double-1>", self.on_tree_double_click)

        # Bind right-click for context menu
        self.tree.bind("<Button-3>", self.show_context_menu)

        # Empty state
        self.show_empty_state()

    def setup_treeview_style(self):
        """Setup custom TreeView styling"""
        style = ttk.Style()
        style.theme_use("default")

        # TreeView style
        style.configure(
            "Custom.Treeview",
            background=Colors.BG_TERTIARY,
            foreground=Colors.TEXT_PRIMARY,
            fieldbackground=Colors.BG_TERTIARY,
            borderwidth=0,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            rowheight=32
        )

        # Heading style
        style.configure(
            "Custom.Treeview.Heading",
            background=Colors.BG_SECONDARY,
            foreground=Colors.TEXT_SECONDARY,
            borderwidth=0,
            relief="flat",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM, "bold")
        )

        # Selected row
        style.map(
            "Custom.Treeview",
            background=[("selected", Colors.ACCENT)],
            foreground=[("selected", Colors.TEXT_PRIMARY)]
        )

    def show_empty_state(self):
        """Show empty state message"""
        self.tree.delete(*self.tree.get_children())
        self.tree.insert(
            "",
            "end",
            text="  No database loaded",
            values=("", ""),
            tags=("empty",)
        )
        self.tree.tag_configure("empty", foreground=Colors.TEXT_MUTED)

    def load_tables(self, db_path):
        """Load tables from database"""
        self.db_path = db_path

        # Clear existing
        self.tree.delete(*self.tree.get_children())

        try:
            from core.db_manager import DatabaseManager

            db = DatabaseManager(db_path)
            conn = db.get_connection()
            cursor = conn.cursor()

            # Get all tables
            cursor.execute("""
                SELECT name FROM sqlite_master
                WHERE type='table' AND name NOT LIKE 'sqlite_%'
                ORDER BY name
            """)

            tables = cursor.fetchall()

            if not tables:
                self.tree.insert(
                    "",
                    "end",
                    text="  No tables found",
                    values=("", ""),
                    tags=("empty",)
                )
                self.tree.tag_configure("empty", foreground=Colors.TEXT_MUTED)
                return

            # Add each table
            for (table_name,) in tables:
                # Get column count
                cursor.execute(f"PRAGMA table_info({table_name})")
                column_count = len(cursor.fetchall())

                # Get row count
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    row_count = cursor.fetchone()[0]
                    row_str = f"{row_count:,}"
                except:
                    row_str = "N/A"

                # Insert into tree
                self.tree.insert(
                    "",
                    "end",
                    text=f"  {table_name}",
                    values=(column_count, row_str)
                )

        except Exception as e:
            self.tree.insert(
                "",
                "end",
                text=f"  Error: {str(e)[:50]}",
                values=("", ""),
                tags=("error",)
            )
            self.tree.tag_configure("error", foreground=Colors.ERROR)

    def refresh_tables(self):
        """Refresh table list"""
        if self.db_path:
            self.load_tables(self.db_path)

    def on_tree_double_click(self, event):
        """Handle double-click on table"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        table_name = item["text"].strip()

        # Call callback if valid table
        if self.on_table_selected and table_name and table_name not in ["No database loaded", "No tables found"]:
            self.on_table_selected(table_name)

    def show_context_menu(self, event):
        """Show context menu on right-click"""
        # Select the item under cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            table_text = self.tree.item(item)["text"].strip()

            # Don't show menu for empty states
            if table_text in ["No database loaded", "No tables found"] or table_text.startswith("Error:"):
                return

            # Create context menu
            from tkinter import Menu
            menu = Menu(self.tree, tearoff=0)
            menu.add_command(label="Open Table", command=lambda: self.on_tree_double_click(None))
            menu.add_command(label="Export to Excel", command=self.export_table)
            menu.add_separator()
            menu.add_command(label="Delete Table", command=self.delete_table)

            menu.post(event.x_root, event.y_root)

    def export_table(self):
        """Export selected table to Excel"""
        selection = self.tree.selection()
        if not selection:
            return

        table_name = self.tree.item(selection[0])["text"].strip()

        from tkinter import filedialog, messagebox
        from core.db_manager import DatabaseManager
        import pandas as pd

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title=f"Export {table_name}",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )

        if not filename:
            return

        try:
            # Read table data
            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

            # Export based on file extension
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
            else:
                df.to_excel(filename, index=False, sheet_name=table_name)

            messagebox.showinfo("Success", f"Table '{table_name}' exported successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export table:\n{str(e)}")

    def delete_table(self):
        """Delete selected table with confirmation"""
        selection = self.tree.selection()
        if not selection:
            return

        table_name = self.tree.item(selection[0])["text"].strip()

        from tkinter import messagebox
        from core.db_manager import DatabaseManager

        # Confirm deletion
        result = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete table '{table_name}'?\n\nThis action cannot be undone.",
            icon='warning'
        )

        if not result:
            return

        try:
            # Delete table
            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DROP TABLE {table_name}")
            conn.commit()

            messagebox.showinfo("Success", f"Table '{table_name}' deleted successfully!")

            # Refresh table list
            self.load_tables(self.db_path)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete table:\n{str(e)}")
