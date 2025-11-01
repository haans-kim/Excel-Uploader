# Excel to SQLite Uploader

Simple Python utility to upload Excel files to SQLite databases.

## Features

- ✅ Load Excel files (.xlsx, .xls)
- ✅ Automatic multi-sheet merging
- ✅ SQLite database creation and table management
- ✅ Memory-efficient chunked uploads
- ✅ Simple CLI interface
- ✅ Ready for Electron integration

## Project Structure

```
Excel-uploader/
├── core/
│   ├── db_manager.py       # SQLite database operations
│   └── excel_loader.py     # Excel file loading
├── upload.py               # Main upload script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python upload.py <excel_file> <table_name> [db_path]
```

**Examples:**

```bash
# Upload to default database (sambio_human.db)
python upload.py data.xlsx employees

# Upload to custom database
python upload.py data.xlsx employees custom.db
```

### Python API

```python
from upload import upload_excel

# Upload Excel file
rows = upload_excel(
    excel_path='data.xlsx',
    table_name='employees',
    db_path='sambio_human.db',
    if_exists='replace'  # or 'append' or 'fail'
)

print(f"Uploaded {rows} rows")
```

## Core Components

### ExcelLoader

Handles Excel file loading with automatic sheet merging:

```python
from core.excel_loader import ExcelLoader

loader = ExcelLoader()
df = loader.load_excel_file('data.xlsx', auto_merge_sheets=True)
```

**Features:**
- Multi-sheet support (automatically merges all sheets)
- Memory optimization
- Type inference

### DatabaseManager

Manages SQLite database operations:

```python
from core.db_manager import DatabaseManager

db = DatabaseManager('sambio_human.db')
db.dataframe_to_table(df, 'table_name', if_exists='replace')
stats = db.get_table_stats('table_name')
db.close()
```

**Features:**
- Chunked inserts (5000 rows per batch)
- Transaction management
- Table statistics
- Date range operations

## Electron Integration

This project is designed to be integrated with Electron apps:

### Example: Electron IPC

```javascript
// In Electron main process
const { spawn } = require('child_process');
const path = require('path');

function uploadExcel(excelPath, tableName) {
  const pythonPath = path.join(__dirname, 'venv/Scripts/python.exe');
  const scriptPath = path.join(__dirname, 'upload.py');

  const process = spawn(pythonPath, [scriptPath, excelPath, tableName]);

  process.stdout.on('data', (data) => {
    console.log(data.toString());
    // Send progress to renderer
    mainWindow.webContents.send('upload-progress', data.toString());
  });

  process.on('close', (code) => {
    if (code === 0) {
      mainWindow.webContents.send('upload-complete');
    } else {
      mainWindow.webContents.send('upload-error', code);
    }
  });
}
```

## Database Schema

The uploader will automatically create tables based on the Excel data structure.

**Example:**

If your Excel has columns: `Name`, `Age`, `Email`

SQLite table will be created with:
```sql
CREATE TABLE employees (
  Name TEXT,
  Age INTEGER,
  Email TEXT
)
```

## Configuration

### Upload Modes

- `replace`: Drop existing table and create new one
- `append`: Add rows to existing table
- `fail`: Raise error if table exists

### Default Database

Default database name: `sambio_human.db`

Change by passing `db_path` parameter:

```bash
python upload.py data.xlsx table_name my_database.db
```

## Requirements

- Python 3.8+
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## Logging

The uploader provides detailed logging:

```
2025-11-01 13:30:15 - INFO - Loading Excel file: data.xlsx
2025-11-01 13:30:16 - INFO - Loaded 1,234 rows with 5 columns
2025-11-01 13:30:16 - INFO - Uploading to table 'employees' (mode: replace)
2025-11-01 13:30:17 - INFO - Progress: 5,000/10,000 rows (50.0%)
2025-11-01 13:30:18 - INFO - ✓ Successfully uploaded 10,000 rows to 'employees'
```

## Error Handling

Common errors and solutions:

### File not found
```
Error: Excel file not found: data.xlsx
Solution: Check file path is correct
```

### Invalid file type
```
Error: Invalid file type. Expected .xlsx or .xls
Solution: Only Excel files are supported
```

### Database locked
```
Error: Database is locked
Solution: Close any other programs accessing the database
```

## Development

### Running Tests

```bash
# Test upload
python upload.py test_data.xlsx test_table test.db
```

### Viewing Database

Use SQLite browser or command line:

```bash
sqlite3 sambio_human.db
sqlite> .tables
sqlite> SELECT * FROM employees LIMIT 10;
```

## License

MIT License

## Support

For issues or questions, please refer to:
- [CLAUDE_CODE_ANALYSIS_USE_CASES.md](CLAUDE_CODE_ANALYSIS_USE_CASES.md) - Usage examples
- [EXCEL_UPLOAD_IMPLEMENTATION_SUMMARY.md](EXCEL_UPLOAD_IMPLEMENTATION_SUMMARY.md) - Implementation details
