#!/usr/bin/env python3
"""
Excel to SQLite Uploader
Simple script to upload Excel files to SQLite database

Usage:
    python upload.py <excel_file> <table_name> [db_path]

Examples:
    python upload.py data.xlsx my_table
    python upload.py data.xlsx my_table custom.db
"""

import sys
import logging
from pathlib import Path
from core.excel_loader import ExcelLoader
from core.db_manager import DatabaseManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def upload_excel(excel_path: str, table_name: str, db_path: str = 'sambio_human.db', if_exists: str = 'replace'):
    """
    Upload Excel file to SQLite database

    Args:
        excel_path: Path to Excel file
        table_name: Target table name
        db_path: SQLite database path (default: sambio_human.db)
        if_exists: What to do if table exists ('replace', 'append', 'fail')

    Returns:
        Number of rows uploaded
    """
    try:
        excel_file = Path(excel_path)
        db_file = Path(db_path)

        # Validate Excel file
        if not excel_file.exists():
            raise FileNotFoundError(f"Excel file not found: {excel_path}")

        if not excel_file.suffix.lower() in ['.xlsx', '.xls']:
            raise ValueError(f"Invalid file type. Expected .xlsx or .xls, got {excel_file.suffix}")

        logger.info(f"Loading Excel file: {excel_file.name}")

        # Load Excel file
        loader = ExcelLoader()
        df = loader.load_excel_file(excel_file, auto_merge_sheets=True)

        logger.info(f"Loaded {len(df):,} rows with {len(df.columns)} columns")
        logger.info(f"Columns: {list(df.columns)}")

        # Create database if it doesn't exist
        if not db_file.exists():
            logger.warning(f"Database file not found. Creating new database: {db_path}")
            db_file.touch()

        # Upload to database
        db = DatabaseManager(str(db_file))
        logger.info(f"Uploading to table '{table_name}' (mode: {if_exists})")

        rows_inserted = db.dataframe_to_table(df, table_name, if_exists=if_exists)

        logger.info(f"✓ Successfully uploaded {rows_inserted:,} rows to '{table_name}'")

        # Show table stats
        stats = db.get_table_stats(table_name)
        logger.info(f"Table '{table_name}' now has {stats['row_count']:,} total rows")

        db.close()
        return rows_inserted

    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise


def main():
    """Command line interface"""
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nError: Missing required arguments")
        print("Usage: python upload.py <excel_file> <table_name> [db_path]")
        sys.exit(1)

    excel_path = sys.argv[1]
    table_name = sys.argv[2]
    db_path = sys.argv[3] if len(sys.argv) > 3 else 'sambio_human.db'

    try:
        upload_excel(excel_path, table_name, db_path)
        print("\n✓ Upload completed successfully!")

    except Exception as e:
        print(f"\n✗ Upload failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
