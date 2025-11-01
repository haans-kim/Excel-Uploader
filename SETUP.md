# Setup Instructions

## Quick Start (Windows)

### 1. Delete Old Virtual Environment

```bash
rmdir /s /q venv
```

### 2. Create Fresh Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Test Installation

```bash
python upload.py --help
```

You should see the usage instructions.

## Quick Start (macOS/Linux)

### 1. Delete Old Virtual Environment

```bash
rm -rf venv
```

### 2. Create Fresh Virtual Environment

```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Test Installation

```bash
python upload.py --help
```

## Verification

After setup, test with a sample Excel file:

```bash
python upload.py sample.xlsx test_table
```

## Troubleshooting

### Python not found
```bash
# Make sure Python 3.8+ is installed
python --version
```

### Permission denied (Windows)
```bash
# Run PowerShell as Administrator, then enable scripts:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### pip install fails
```bash
# Upgrade pip first
python -m pip install --upgrade pip
pip install -r requirements.txt
```
