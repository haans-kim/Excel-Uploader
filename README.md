# SQLite Manager

Modern desktop application for managing SQLite databases with Excel import functionality.

## Features

- 📊 **Database Management** - Create, open, and browse SQLite databases
- 📁 **Table Operations** - Create, delete, and export tables
- 📈 **Excel Import** - Upload Excel files with multi-sheet support
- 🔍 **Data Browser** - View, search, sort, and paginate table data
- 🎨 **Modern UI** - Clean interface with dark/light theme support
- 💻 **Standalone Executable** - No Python installation required

## Quick Start

### Option 1: Run Executable (Recommended)

1. Navigate to `build\exe.win-amd64-3.10\`
2. Double-click `SQLiteManager.exe`
3. No installation required!

### Option 2: Run from Source

**Requirements:**
- Python 3.10+
- Windows, macOS, or Linux

**Steps:**

1. Create virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run application:
```bash
python main.py
```

Or use the launcher:
```bash
start.bat
```

## Building Executable

To create a standalone executable:

```bash
build-cx-freeze.bat
```

Output will be in `build\exe.win-amd64-3.10\`

**Distribution:**
Copy the entire `build\exe.win-amd64-3.10\` folder to distribute the application.

## Project Structure

```
Excel-uploader/
├── build/                      # Build output
│   └── exe.win-amd64-3.10/    # Executable distribution
├── core/                       # Backend logic
│   ├── db_manager.py          # Database operations
│   └── excel_loader.py        # Excel file handling
├── ui/                         # User interface
│   ├── main_window.py         # Main application window
│   ├── styles.py              # UI color scheme and styles
│   └── components/            # UI components
│       ├── database_selector.py
│       ├── table_browser.py
│       ├── table_creator.py
│       ├── table_list.py
│       └── excel_uploader.py
├── main.py                     # Application entry point
├── setup.py                    # cx_Freeze build configuration
├── build-cx-freeze.bat        # Build script
├── start.bat                  # Development launcher
└── requirements.txt           # Python dependencies
```

## Usage

### Opening a Database

1. Click **"Open Database"** or use the sidebar
2. Select an existing `.db` file
3. Database info will display in the header

### Creating a Database

1. Click **"New Database"** or use the sidebar
2. Choose location and name
3. Database is created and opened automatically

### Uploading Excel Files

1. Open a database first
2. Click **"Upload Excel"** in the sidebar
3. Select your Excel file (.xlsx, .xls)
4. Choose which sheets to import
5. Specify table names for each sheet
6. Click **"Upload"**

**Features:**
- Multi-sheet support
- Progress tracking
- Automatic type detection
- Chunked uploads for large files

### Browsing Tables

1. Click **"Browse Tables"** in the sidebar
2. Select a table from the list
3. View data with:
   - Search functionality
   - Column sorting
   - Pagination (50 rows per page)
   - Export to Excel

### Creating Tables

1. Click **"Create Table"** in the sidebar
2. Enter table name
3. Add columns with name and type
4. Click **"Create Table"**

## Theme Support

Toggle between light and dark themes:
- Click the theme button in the sidebar
- Setting persists across sessions
- All UI elements adapt automatically

## Technical Details

### Built With

- **CustomTkinter** - Modern UI framework
- **pandas** - Data processing
- **openpyxl** - Excel file handling
- **SQLite3** - Database engine
- **cx_Freeze** - Executable packaging

### Performance

- **Startup Time:** ~0.5 seconds
- **Memory Footprint:** ~30MB
- **Executable Size:** ~22KB (+ dependencies)
- **Chunked Uploads:** 5000 rows per batch

### Database Operations

- Transaction-safe inserts
- Automatic schema detection
- Foreign key support
- Index management

## Requirements

**Runtime (Executable):**
- Windows 10 or later
- No Python installation needed

**Development:**
- Python 3.10+
- See `requirements.txt` for dependencies

## Troubleshooting

### Application won't start
- Ensure all files in `build\exe.win-amd64-3.10\` are present
- Check antivirus isn't blocking the executable

### Database locked error
- Close any other programs using the database
- Ensure you have write permissions

### Excel import fails
- Verify Excel file is not corrupted
- Check file uses .xlsx or .xls extension
- Ensure Excel file is not open in another program

## Development

### Running in Development Mode

```bash
# Activate virtual environment
venv\Scripts\activate

# Run application
python main.py
```

### Making Changes

After modifying code, rebuild the executable:

```bash
build-cx-freeze.bat
```

## License

MIT License

## Credits

Built with Claude Code
