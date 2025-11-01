"""
Excel Uploader Component
Upload Excel files to database
"""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from ui.styles import Colors, Styles


class ExcelUploader(ctk.CTkToplevel):
    """Excel upload dialog"""

    def __init__(self, parent, db_path, on_complete_callback=None):
        super().__init__(parent)

        self.db_path = db_path
        self.on_complete = on_complete_callback
        self.excel_file = None
        self.sheet_names = []

        # Window configuration
        self.title("Upload Excel File")
        self.geometry("600x500")
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
            text="Upload Excel to Database",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(pady=(0, 20))

        # File selection
        file_frame = ctk.CTkFrame(container, fg_color=Colors.BG_SECONDARY)
        file_frame.pack(fill="x", pady=(0, 20))

        file_label = ctk.CTkLabel(
            file_frame,
            text="Excel File:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            text_color=Colors.TEXT_SECONDARY
        )
        file_label.pack(padx=Styles.PADDING, pady=(Styles.PADDING, 5), anchor="w")

        self.file_path_label = ctk.CTkLabel(
            file_frame,
            text="No file selected",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_MUTED,
            anchor="w"
        )
        self.file_path_label.pack(padx=Styles.PADDING, pady=(0, 10), anchor="w", fill="x")

        browse_btn = ctk.CTkButton(
            file_frame,
            text="Browse...",
            command=self.browse_file,
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER
        )
        browse_btn.pack(padx=Styles.PADDING, pady=(0, Styles.PADDING))

        # Sheet selection (hidden initially)
        self.sheet_frame = ctk.CTkFrame(container, fg_color=Colors.BG_SECONDARY)

        sheet_label = ctk.CTkLabel(
            self.sheet_frame,
            text="Select Sheets to Import:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            text_color=Colors.TEXT_SECONDARY
        )
        sheet_label.pack(padx=Styles.PADDING, pady=(Styles.PADDING, 10), anchor="w")

        # Scrollable frame for sheet checkboxes
        self.sheet_scroll = ctk.CTkScrollableFrame(
            self.sheet_frame,
            height=150,
            fg_color=Colors.BG_TERTIARY
        )
        self.sheet_scroll.pack(padx=Styles.PADDING, pady=(0, Styles.PADDING), fill="both", expand=True)

        # Options
        options_frame = ctk.CTkFrame(container, fg_color=Colors.BG_SECONDARY)
        options_frame.pack(fill="x", pady=(0, 20))

        options_label = ctk.CTkLabel(
            options_frame,
            text="Options:",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE),
            text_color=Colors.TEXT_SECONDARY
        )
        options_label.pack(padx=Styles.PADDING, pady=(Styles.PADDING, 10), anchor="w")

        self.if_exists_var = ctk.StringVar(value="append")

        radio_frame = ctk.CTkFrame(options_frame, fg_color="transparent")
        radio_frame.pack(padx=Styles.PADDING, pady=(0, Styles.PADDING), fill="x")

        append_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Append to existing table",
            variable=self.if_exists_var,
            value="append",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_PRIMARY
        )
        append_radio.pack(anchor="w", pady=2)

        replace_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Replace existing table",
            variable=self.if_exists_var,
            value="replace",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_PRIMARY
        )
        replace_radio.pack(anchor="w", pady=2)

        fail_radio = ctk.CTkRadioButton(
            radio_frame,
            text="Fail if table exists",
            variable=self.if_exists_var,
            value="fail",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_PRIMARY
        )
        fail_radio.pack(anchor="w", pady=2)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            container,
            height=10,
            corner_radius=Styles.CORNER_RADIUS_SM
        )
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(
            container,
            text="",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY
        )

        # Buttons
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(fill="x", pady=(10, 0))

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

        self.upload_btn = ctk.CTkButton(
            button_frame,
            text="Upload",
            command=self.upload,
            width=120,
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.SUCCESS,
            hover_color=Colors.SUCCESS_HOVER,
            state="disabled"
        )
        self.upload_btn.pack(side="right")

    def browse_file(self):
        """Browse for Excel file"""
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[
                ("Excel files", "*.xlsx;*.xls"),
                ("All files", "*.*")
            ]
        )

        if filename:
            self.excel_file = filename
            self.file_path_label.configure(text=filename)
            self.load_sheets()
            self.upload_btn.configure(state="normal")

    def load_sheets(self):
        """Load sheet names from Excel file"""
        from core.excel_loader import load_excel_file

        try:
            # Load Excel file to get sheet names
            sheets_data = load_excel_file(self.excel_file)
            self.sheet_names = list(sheets_data.keys())

            # Show sheet selection
            self.sheet_frame.pack(fill="both", expand=True, pady=(0, 20))

            # Clear existing checkboxes
            for widget in self.sheet_scroll.winfo_children():
                widget.destroy()

            # Create checkbox for each sheet
            self.sheet_vars = {}
            for sheet_name in self.sheet_names:
                var = ctk.BooleanVar(value=True)
                self.sheet_vars[sheet_name] = var

                cb = ctk.CTkCheckBox(
                    self.sheet_scroll,
                    text=sheet_name,
                    variable=var,
                    font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
                    text_color=Colors.TEXT_PRIMARY
                )
                cb.pack(anchor="w", pady=5, padx=10)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")
            self.excel_file = None
            self.file_path_label.configure(text="No file selected")
            self.upload_btn.configure(state="disabled")

    def upload(self):
        """Upload selected sheets to database"""
        if not self.excel_file:
            return

        # Get selected sheets
        selected_sheets = [
            sheet for sheet, var in self.sheet_vars.items()
            if var.get()
        ]

        if not selected_sheets:
            messagebox.showwarning("No Sheets", "Please select at least one sheet to import.")
            return

        # Show progress
        self.progress.pack(fill="x", pady=(0, 5))
        self.progress_label.pack(fill="x")

        # Disable buttons
        self.upload_btn.configure(state="disabled")

        try:
            from core.excel_loader import load_excel_file
            from core.db_manager import DatabaseManager

            # Load Excel data
            self.progress_label.configure(text="Loading Excel file...")
            self.progress.set(0.2)
            self.update()

            sheets_data = load_excel_file(self.excel_file)

            # Upload each selected sheet
            db = DatabaseManager(self.db_path)
            if_exists = self.if_exists_var.get()

            total = len(selected_sheets)
            for i, sheet_name in enumerate(selected_sheets):
                self.progress_label.configure(text=f"Uploading {sheet_name}...")
                self.progress.set(0.2 + (0.7 * (i / total)))
                self.update()

                df = sheets_data[sheet_name]
                db.dataframe_to_table(df, sheet_name, if_exists=if_exists)

            # Complete
            self.progress.set(1.0)
            self.progress_label.configure(text="Upload complete!")
            self.update()

            messagebox.showinfo(
                "Success",
                f"Successfully uploaded {total} sheet(s) to database."
            )

            # Call completion callback
            if self.on_complete:
                self.on_complete()

            # Close dialog
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload Excel file:\n{str(e)}")
            self.upload_btn.configure(state="normal")
            self.progress.pack_forget()
            self.progress_label.pack_forget()

    def cancel(self):
        """Cancel and close dialog"""
        self.destroy()
