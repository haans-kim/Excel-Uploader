"""
Create a test Excel file with sample data
"""
import pandas as pd
from pathlib import Path

def create_test_excel():
    """Create test Excel file with multiple sheets"""
    output_file = Path(__file__).parent / "test_data.xlsx"

    # Create Excel writer
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Sheet 1: Products
        products = pd.DataFrame({
            'product_id': [1, 2, 3, 4, 5],
            'product_name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam'],
            'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Electronics'],
            'price': [1200.00, 25.00, 75.00, 350.00, 89.99],
            'stock': [15, 100, 50, 30, 45]
        })
        products.to_excel(writer, sheet_name='products', index=False)

        # Sheet 2: Customers
        customers = pd.DataFrame({
            'customer_id': [1, 2, 3, 4],
            'first_name': ['John', 'Jane', 'Bob', 'Alice'],
            'last_name': ['Doe', 'Smith', 'Johnson', 'Williams'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
            'city': ['New York', 'Los Angeles', 'Chicago', 'Houston']
        })
        customers.to_excel(writer, sheet_name='customers', index=False)

        # Sheet 3: Orders
        orders = pd.DataFrame({
            'order_id': [101, 102, 103, 104, 105],
            'customer_id': [1, 2, 1, 3, 4],
            'product_id': [1, 2, 3, 1, 4],
            'quantity': [1, 2, 1, 1, 2],
            'order_date': pd.to_datetime(['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19']),
            'total_amount': [1200.00, 50.00, 75.00, 1200.00, 700.00]
        })
        orders.to_excel(writer, sheet_name='orders', index=False)

    print(f"Test Excel file created: {output_file}")
    print(f"   - 3 sheets created")
    print(f"   - products: 5 rows")
    print(f"   - customers: 4 rows")
    print(f"   - orders: 5 rows")

if __name__ == "__main__":
    create_test_excel()
