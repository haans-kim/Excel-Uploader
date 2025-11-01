"""
Table Browser Component
View and browse table data with pagination
"""
import customtkinter as ctk
from tkinter import ttk
from ui.styles import Colors, Styles


class TableBrowser(ctk.CTkFrame):
    """Table data browser with pagination"""

    def __init__(self, parent, db_path, table_name):
        super().__init__(
            parent,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )

        self.db_path = db_path
        self.table_name = table_name
        self.current_page = 0
        self.rows_per_page = 50
        self.total_rows = 0
        self.columns = []
        self.search_text = ""
        self.sort_column = None
        self.sort_order = "ASC"

        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup the UI components"""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=Styles.PADDING, pady=(Styles.PADDING, 10))

        # Back button
        back_btn = ctk.CTkButton(
            header,
            text="← Back",
            width=80,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.on_back
        )
        back_btn.pack(side="left", padx=(0, 10))

        # Table name
        title = ctk.CTkLabel(
            header,
            text=f"Table: {self.table_name}",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_LG, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(side="left")

        # Export button
        export_btn = ctk.CTkButton(
            header,
            text="Export",
            width=80,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.SUCCESS,
            hover_color=Colors.SUCCESS_HOVER,
            command=self.export_data
        )
        export_btn.pack(side="right", padx=(0, 10))

        # Row count
        self.row_count_label = ctk.CTkLabel(
            header,
            text="",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY
        )
        self.row_count_label.pack(side="right", padx=(0, 10))

        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=Styles.PADDING, pady=(0, 10))

        search_label = ctk.CTkLabel(
            search_frame,
            text="Search:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY
        )
        search_label.pack(side="left", padx=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search in all columns...",
            height=Styles.INPUT_HEIGHT_SM,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.search_entry.bind("<Return>", lambda e: self.apply_search())

        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            width=80,
            height=Styles.INPUT_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            command=self.apply_search
        )
        search_btn.pack(side="left", padx=(0, 5))

        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            width=60,
            height=Styles.INPUT_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.clear_search
        )
        clear_btn.pack(side="left")

        # TreeView container
        tree_container = ctk.CTkFrame(self, fg_color="transparent")
        tree_container.pack(fill="both", expand=True, padx=Styles.PADDING, pady=(0, 10))

        # Create TreeView (will configure columns after loading data)
        self.tree = ttk.Treeview(
            tree_container,
            show="headings",
            style="Custom.Treeview",
            selectmode="browse"
        )

        # Scrollbars
        vsb = ctk.CTkScrollbar(tree_container, command=self.tree.yview)
        hsb = ctk.CTkScrollbar(tree_container, orientation="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Pack
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        # Pagination controls
        pagination = ctk.CTkFrame(self, fg_color="transparent")
        pagination.pack(fill="x", padx=Styles.PADDING, pady=(0, Styles.PADDING))

        self.prev_btn = ctk.CTkButton(
            pagination,
            text="← Previous",
            width=100,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.prev_page
        )
        self.prev_btn.pack(side="left", padx=(0, 10))

        self.page_label = ctk.CTkLabel(
            pagination,
            text="",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY
        )
        self.page_label.pack(side="left", padx=10)

        self.next_btn = ctk.CTkButton(
            pagination,
            text="Next →",
            width=100,
            height=Styles.BUTTON_HEIGHT_SM,
            corner_radius=Styles.CORNER_RADIUS_SM,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.next_page
        )
        self.next_btn.pack(side="left")

        # Setup TreeView style
        self.setup_treeview_style()

    def setup_treeview_style(self):
        """Setup custom TreeView styling"""
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Custom.Treeview",
            background=Colors.BG_TERTIARY,
            foreground=Colors.TEXT_PRIMARY,
            fieldbackground=Colors.BG_TERTIARY,
            borderwidth=0,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            rowheight=28
        )

        style.configure(
            "Custom.Treeview.Heading",
            background=Colors.BG_SECONDARY,
            foreground=Colors.TEXT_SECONDARY,
            borderwidth=0,
            relief="flat",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM, "bold")
        )

        style.map(
            "Custom.Treeview",
            background=[("selected", Colors.ACCENT)],
            foreground=[("selected", Colors.TEXT_PRIMARY)]
        )

    def load_data(self):
        """Load table data"""
        from core.db_manager import DatabaseManager

        try:
            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            cursor = conn.cursor()

            # Get column names
            cursor.execute(f"PRAGMA table_info({self.table_name})")
            columns_info = cursor.fetchall()
            self.columns = [col[1] for col in columns_info]

            # Configure TreeView columns
            self.tree["columns"] = self.columns
            for col in self.columns:
                self.tree.heading(
                    col,
                    text=col,
                    command=lambda c=col: self.sort_by_column(c)
                )
                self.tree.column(col, width=120, minwidth=80)

            # Get total row count (with search filter if applied)
            count_query = f"SELECT COUNT(*) FROM {self.table_name}"
            if self.search_text:
                where_clauses = [f"{col} LIKE ?" for col in self.columns]
                count_query += f" WHERE {' OR '.join(where_clauses)}"
                search_params = [f"%{self.search_text}%"] * len(self.columns)
                cursor.execute(count_query, search_params)
            else:
                cursor.execute(count_query)
            self.total_rows = cursor.fetchone()[0]

            # Load first page
            self.load_page()

        except Exception as e:
            self.row_count_label.configure(text=f"Error: {str(e)[:50]}")

    def load_page(self):
        """Load current page of data"""
        from core.db_manager import DatabaseManager

        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            cursor = conn.cursor()

            # Calculate offset
            offset = self.current_page * self.rows_per_page

            # Build query with search and sort
            query = f"SELECT * FROM {self.table_name}"
            params = []

            # Add WHERE clause for search
            if self.search_text:
                where_clauses = [f"{col} LIKE ?" for col in self.columns]
                query += f" WHERE {' OR '.join(where_clauses)}"
                params = [f"%{self.search_text}%"] * len(self.columns)

            # Add ORDER BY clause for sorting
            if self.sort_column:
                query += f" ORDER BY {self.sort_column} {self.sort_order}"

            # Add LIMIT and OFFSET
            query += " LIMIT ? OFFSET ?"
            params.extend([self.rows_per_page, offset])

            # Fetch data for current page
            cursor.execute(query, params)
            rows = cursor.fetchall()

            # Insert data into tree
            for row in rows:
                # Convert None to empty string and limit length
                display_row = []
                for value in row:
                    if value is None:
                        display_row.append("NULL")
                    else:
                        str_value = str(value)
                        # Truncate long values
                        if len(str_value) > 100:
                            display_row.append(str_value[:97] + "...")
                        else:
                            display_row.append(str_value)

                self.tree.insert("", "end", values=display_row)

            # Update pagination controls
            self.update_pagination()

        except Exception as e:
            print(f"Error loading page: {e}")

    def update_pagination(self):
        """Update pagination controls"""
        total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page

        # Update labels
        self.row_count_label.configure(text=f"{self.total_rows:,} rows")
        self.page_label.configure(
            text=f"Page {self.current_page + 1} of {total_pages}"
        )

        # Enable/disable buttons
        self.prev_btn.configure(state="normal" if self.current_page > 0 else "disabled")
        self.next_btn.configure(
            state="normal" if self.current_page < total_pages - 1 else "disabled"
        )

    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page()

    def next_page(self):
        """Go to next page"""
        total_pages = (self.total_rows + self.rows_per_page - 1) // self.rows_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.load_page()

    def apply_search(self):
        """Apply search filter"""
        self.search_text = self.search_entry.get().strip()
        self.current_page = 0  # Reset to first page
        self.load_data()  # Reload with new search

    def clear_search(self):
        """Clear search filter"""
        self.search_entry.delete(0, 'end')
        self.search_text = ""
        self.current_page = 0
        self.load_data()

    def sort_by_column(self, column):
        """Sort by clicked column"""
        # Toggle sort order if same column
        if self.sort_column == column:
            self.sort_order = "DESC" if self.sort_order == "ASC" else "ASC"
        else:
            self.sort_column = column
            self.sort_order = "ASC"

        # Update column heading to show sort direction
        for col in self.columns:
            if col == column:
                arrow = " ↑" if self.sort_order == "ASC" else " ↓"
                self.tree.heading(col, text=f"{col}{arrow}")
            else:
                self.tree.heading(col, text=col)

        self.current_page = 0
        self.load_page()

    def export_data(self):
        """Export table data to Excel or CSV"""
        from tkinter import filedialog, messagebox
        import pandas as pd

        # Ask for save location
        filename = filedialog.asksaveasfilename(
            title=f"Export {self.table_name}",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("CSV files", "*.csv")]
        )

        if not filename:
            return

        try:
            from core.db_manager import DatabaseManager

            # Read all table data (not just current page)
            db = DatabaseManager(self.db_path)
            conn = db.get_connection()
            df = pd.read_sql_query(f"SELECT * FROM {self.table_name}", conn)

            # Export based on file extension
            if filename.endswith('.csv'):
                df.to_csv(filename, index=False)
            else:
                df.to_excel(filename, index=False, sheet_name=self.table_name)

            messagebox.showinfo("Success", f"Exported {len(df):,} rows to {filename}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data:\n{str(e)}")

    def on_back(self):
        """Handle back button"""
        # Will be set by parent
        pass
