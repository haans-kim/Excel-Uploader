"""
Create a test SQLite database with sample data
"""
import sqlite3
from pathlib import Path

def create_test_database():
    """Create test database with sample tables"""
    db_path = Path(__file__).parent / "test_data.db"

    # Remove if exists
    if db_path.exists():
        db_path.unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create employees table
    cursor.execute("""
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            department TEXT,
            salary REAL,
            hire_date DATE
        )
    """)

    # Insert sample data
    employees = [
        ("John Doe", "john@example.com", "Engineering", 85000, "2020-01-15"),
        ("Jane Smith", "jane@example.com", "Marketing", 72000, "2021-03-20"),
        ("Bob Johnson", "bob@example.com", "Engineering", 90000, "2019-06-10"),
        ("Alice Williams", "alice@example.com", "Sales", 68000, "2021-08-05"),
        ("Charlie Brown", "charlie@example.com", "HR", 62000, "2022-02-14"),
    ]

    cursor.executemany(
        "INSERT INTO employees (name, email, department, salary, hire_date) VALUES (?, ?, ?, ?, ?)",
        employees
    )

    # Create departments table
    cursor.execute("""
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            manager TEXT,
            budget REAL
        )
    """)

    departments = [
        ("Engineering", "Bob Johnson", 500000),
        ("Marketing", "Jane Smith", 250000),
        ("Sales", "Alice Williams", 350000),
        ("HR", "Charlie Brown", 150000),
    ]

    cursor.executemany(
        "INSERT INTO departments (name, manager, budget) VALUES (?, ?, ?)",
        departments
    )

    # Create projects table
    cursor.execute("""
        CREATE TABLE projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            start_date DATE,
            end_date DATE,
            status TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        )
    """)

    projects = [
        ("Website Redesign", "Redesign company website", "2024-01-01", "2024-06-30", "In Progress", 1),
        ("Q1 Campaign", "Q1 marketing campaign", "2024-01-01", "2024-03-31", "Completed", 2),
        ("Sales Automation", "Automate sales pipeline", "2024-02-01", "2024-08-31", "Planning", 3),
    ]

    cursor.executemany(
        "INSERT INTO projects (name, description, start_date, end_date, status, department_id) VALUES (?, ?, ?, ?, ?, ?)",
        projects
    )

    conn.commit()
    conn.close()

    print(f"Test database created: {db_path}")
    print(f"   - 3 tables created")
    print(f"   - employees: 5 rows")
    print(f"   - departments: 4 rows")
    print(f"   - projects: 3 rows")

if __name__ == "__main__":
    create_test_database()
