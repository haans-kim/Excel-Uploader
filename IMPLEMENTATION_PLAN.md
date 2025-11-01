# Excel to SQLite Manager - 구현 계획서 (CustomTkinter)

> **목표**: SQLite 데이터베이스 관리 및 Excel 업로드를 위한 Python 데스크톱 애플리케이션
>
> **UI 스타일**: shadcn/ui 스타일의 깔끔한 모던 인터페이스
>
> **기술 스택**: Python + CustomTkinter (최소 오버헤드)

---

## 📋 목차

1. [아키텍처 선택 배경](#아키텍처-선택-배경)
2. [핵심 요구사항 분석](#핵심-요구사항-분석)
3. [Use Case 분석](#use-case-분석)
4. [아키텍처 설계](#아키텍처-설계)
5. [UI/UX 설계](#uiux-설계)
6. [구현 단계별 계획](#구현-단계별-계획)
7. [기술 스택 상세](#기술-스택-상세)
8. [프로젝트 구조](#프로젝트-구조)

---

## 아키텍처 선택 배경

### 🔍 Electron vs CustomTkinter 비교

| 비교 항목 | Electron + React | **CustomTkinter** ⭐ |
|----------|------------------|---------------------|
| **배포 크기** | 200MB+ | **30MB** (7배 작음) |
| **메모리 사용** | 200-300MB | **50-80MB** (4배 적음) |
| **시작 속도** | 3-5초 | **0.5초** (6-10배 빠름) |
| **개발 언어** | TypeScript + Python | **Python만** |
| **구조 복잡도** | 높음 (3계층) | **낮음 (단일)** |
| **shadcn/ui 스타일** | 100% | **95%** |
| **개발 기간** | 7주 | **3주** (절반) |

### ✅ CustomTkinter 선택 이유

1. **최소 오버헤드**: 30MB 단일 실행 파일
2. **단순한 구조**: Python만 사용, IPC 통신 불필요
3. **빠른 시작**: 0.5초 즉시 실행
4. **shadcn/ui 스타일**: 모던한 디자인 시스템 내장
5. **빠른 개발**: 3주 완성 (Electron 대비 절반)
6. **쉬운 유지보수**: 단일 코드베이스

---

## 핵심 요구사항 분석

### 1️⃣ DB 관리 기능
- ✅ **DB 생성/선택**: 새 DB 파일 생성 또는 기존 DB 열기
- ✅ **DB 정보 표시**: 파일 경로, 크기, 테이블 수
- ✅ **최근 DB 목록**: 빠른 접근

### 2️⃣ 테이블 관리 기능
- ✅ **테이블 목록 표시**:
  - 테이블명
  - 컬럼 수
  - 행 수
  - 관련 View/Index
- ✅ **테이블 생성**: 컬럼명, 타입, 제약조건 정의
- ✅ **테이블 수정**: 컬럼 추가/삭제
- ✅ **테이블 삭제**: 안전 삭제 (확인)

### 3️⃣ Excel 업로드 기능
- ✅ **파일 선택**: 파일 다이얼로그
- ✅ **자동 스키마 감지**: Excel → SQLite 매핑
- ✅ **업로드 옵션**: Replace / Append / Replace Range
- ✅ **진행률 표시**: 실시간 업로드 상황
- ✅ **다중 시트 지원**: 자동 병합

### 4️⃣ 데이터 조회 기능
- ✅ **테이블 브라우저**: 페이지네이션
- ✅ **정렬**: 컬럼 클릭
- ✅ **필터링**: 검색
- ✅ **통계 정보**: 행 수, 날짜 범위

### 5️⃣ SQL 쿼리 기능 (선택)
- ⚠️ **SQL 에디터**: 커스텀 쿼리 실행
- ⚠️ **결과 내보내기**: CSV/Excel

---

## Use Case 분석

### 📊 Use Case 1: 데이터 분석가 - 정기 데이터 업로드

**시나리오**: 매월 HR 데이터를 Excel로 받아서 SQLite에 업로드

1. 앱 실행 → 최근 DB 목록에서 `sambio_human.db` 선택
2. 테이블 목록에서 `tag_data` 확인 (현재 120만 행)
3. "Upload Excel" 버튼 클릭
4. Excel 파일 선택
5. 업로드 옵션: "Replace date range" 선택
   - 파일의 날짜 범위 자동 감지 (2025-10-01 ~ 2025-10-31)
6. "Upload" 클릭 → 진행률 바 표시 (30초 소요)
7. 완료 → 테이블 통계 업데이트 (125만 행)
8. Claude Code 실행하여 분석

**필요 UI**:
- 최근 DB 목록 (카드)
- 테이블 목록 (TreeView)
- Excel 업로드 다이얼로그
- 진행률 바

### 📈 Use Case 2: DB 관리자 - 새 프로젝트 셋업

**시나리오**: 신규 프로젝트 DB 구조 설계

1. "Create New Database" 클릭 → `project_data.db` 생성
2. "Create Table" 클릭
   - 테이블명: `employees`
   - 컬럼 추가:
     - `id` INTEGER PRIMARY KEY
     - `name` TEXT NOT NULL
     - `email` TEXT UNIQUE
3. SQL 미리보기 확인
4. "Create" 클릭
5. Excel 업로드 (직원 목록)
6. 테이블 브라우저로 데이터 확인

**필요 UI**:
- DB 생성 다이얼로그
- 테이블 생성 다이얼로그 (컬럼 추가/제거)
- SQL 미리보기 (읽기 전용 텍스트)

### 🔍 Use Case 3: 데이터 조회 및 내보내기

**시나리오**: 특정 조건 데이터 추출

1. `claim_data` 테이블 선택
2. 테이블 브라우저 열림
3. 검색 필터: "Plant 5"
4. 정렬: 근무시간 내림차순
5. 결과 확인
6. (선택) "Export to CSV" 클릭

**필요 UI**:
- 테이블 브라우저 (페이지네이션)
- 검색 입력창
- 정렬 기능 (컬럼 클릭)

---

## 아키텍처 설계

### 🏗️ 전체 아키텍처 (단순화)

```
┌─────────────────────────────────────────┐
│        Python Application               │
│  ┌───────────────────────────────────┐  │
│  │  CustomTkinter UI Layer           │  │
│  │  ┌─────────────────────────────┐  │  │
│  │  │  Components                 │  │  │
│  │  │  - DatabaseSelector         │  │  │
│  │  │  - TableList                │  │  │
│  │  │  - TableBrowser             │  │  │
│  │  │  - ExcelUploader            │  │  │
│  │  │  - TableEditor              │  │  │
│  │  └─────────────────────────────┘  │  │
│  └───────────────┬───────────────────┘  │
│                  │ Direct Call           │
│  ┌───────────────▼───────────────────┐  │
│  │  Core Business Logic              │  │
│  │  - db_manager.py (기존)           │  │
│  │  - excel_loader.py (기존)         │  │
│  └───────────────┬───────────────────┘  │
└──────────────────┼──────────────────────┘
                   │
              ┌────▼────┐
              │ SQLite  │
              └─────────┘

메모리: 50-80MB
크기: 30MB
언어: Python만
```

**Electron 아키텍처와 비교**:
- ❌ IPC 통신 불필요
- ❌ JSON-RPC 서버 불필요
- ❌ 프로세스 간 통신 불필요
- ✅ 직접 함수 호출
- ✅ 단일 프로세스

### 📊 데이터 모델

```python
# Python 클래스 (간단)

class Database:
    def __init__(self, path: str):
        self.path = path
        self.name = Path(path).name
        self.size = Path(path).stat().st_size
        self.table_count = 0

class Table:
    def __init__(self, name: str):
        self.name = name
        self.column_count = 0
        self.row_count = 0
        self.columns: List[Column] = []

class Column:
    def __init__(self, name: str, type: str):
        self.name = name
        self.type = type  # INTEGER, TEXT, REAL, DATE, DATETIME
        self.nullable = True
        self.primary_key = False
        self.unique = False
        self.default_value = None
```

---

## UI/UX 설계

### 🎨 레이아웃 구조

```
┌────────────────────────────────────────────────────────────┐
│  Title: SQLite Manager                      [─] [□] [×]    │
├──────────────┬─────────────────────────────────────────────┤
│              │                                              │
│   Sidebar    │  Main Content Area                          │
│   (200px)    │                                              │
│              │  ┌────────────────────────────────────────┐ │
│  ┌────────┐  │  │  Database Info Card                   │ │
│  │Database│  │  │  📁 sambio_human.db (7.6 GB)         │ │
│  │        │  │  │  📊 12 tables, 1.2M rows             │ │
│  │ [Open] │  │  └────────────────────────────────────────┘ │
│  │ [New]  │  │                                              │
│  └────────┘  │  ┌────────────────────────────────────────┐ │
│              │  │  Table List                            │ │
│  Recent DBs  │  │  ┌──────────────────────────────────┐ │ │
│  • sambio... │  │  │ ☑ tag_data      8 cols  1.2M    │ │ │
│  • project.. │  │  │   claim_data   12 cols   45K    │ │ │
│              │  │  │   employees    10 cols    5K    │ │ │
│  ┌────────┐  │  │  └──────────────────────────────────┘ │ │
│  │ Tables │  │  └────────────────────────────────────────┘ │
│  │        │  │                                              │
│  │[Browse]│  │  ┌────────────────────────────────────────┐ │
│  │[Create]│  │  │  Action Buttons                        │ │
│  │[Upload]│  │  │  [Upload Excel] [Export] [Browse]      │ │
│  └────────┘  │  └────────────────────────────────────────┘ │
└──────────────┴─────────────────────────────────────────────┘
```

### 🧩 CustomTkinter 컴포넌트 설계

#### 색상 시스템 (shadcn/ui 스타일)

```python
# ui/styles.py
class Colors:
    # shadcn/ui zinc palette (dark mode)
    BG_PRIMARY = "#09090b"      # zinc-950
    BG_SECONDARY = "#18181b"    # zinc-900
    BG_TERTIARY = "#27272a"     # zinc-800

    BORDER = "#3f3f46"          # zinc-700
    TEXT_PRIMARY = "#fafafa"    # zinc-50
    TEXT_SECONDARY = "#a1a1aa"  # zinc-400

    ACCENT = "#3b82f6"          # blue-500
    ACCENT_HOVER = "#2563eb"    # blue-600

    SUCCESS = "#22c55e"         # green-500
    ERROR = "#ef4444"           # red-500
    WARNING = "#f59e0b"         # amber-500

class Styles:
    CORNER_RADIUS = 8
    BORDER_WIDTH = 1

    BUTTON_HEIGHT = 40
    INPUT_HEIGHT = 40

    FONT_FAMILY = "Segoe UI"
    FONT_SIZE_SM = 12
    FONT_SIZE_BASE = 14
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 20
```

#### 1. Main Window

```python
import customtkinter as ctk
from ui.styles import Colors, Styles

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("SQLite Manager")
        self.geometry("1400x900")
        ctk.set_appearance_mode("dark")

        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = Sidebar(self)
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main content
        self.main_content = MainContent(self)
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
```

#### 2. Database Selector Card

```python
class DatabaseCard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )

        # Database icon + name
        self.label = ctk.CTkLabel(
            self,
            text="📁 sambio_human.db",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        self.label.pack(padx=20, pady=(20, 10))

        # Stats
        self.stats = ctk.CTkLabel(
            self,
            text="7.6 GB • 12 tables • 1.2M rows",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_SM),
            text_color=Colors.TEXT_SECONDARY
        )
        self.stats.pack(padx=20, pady=(0, 10))

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=20, pady=(0, 20))

        self.btn_open = ctk.CTkButton(
            btn_frame,
            text="Open DB",
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            command=self.open_db
        )
        self.btn_open.pack(side="left", padx=5)

        self.btn_new = ctk.CTkButton(
            btn_frame,
            text="New DB",
            height=Styles.BUTTON_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            command=self.create_db
        )
        self.btn_new.pack(side="left", padx=5)
```

#### 3. Table List (TreeView)

```python
import tkinter as tk
from tkinter import ttk

class TableList(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            corner_radius=Styles.CORNER_RADIUS,
            fg_color=Colors.BG_SECONDARY,
            border_width=Styles.BORDER_WIDTH,
            border_color=Colors.BORDER
        )

        # Title
        title = ctk.CTkLabel(
            self,
            text="Tables",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_LG, "bold"),
            text_color=Colors.TEXT_PRIMARY
        )
        title.pack(padx=20, pady=(20, 10), anchor="w")

        # Treeview (스타일 커스터마이징)
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.Treeview",
            background=Colors.BG_TERTIARY,
            foreground=Colors.TEXT_PRIMARY,
            fieldbackground=Colors.BG_TERTIARY,
            borderwidth=0,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE)
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=Colors.BG_SECONDARY,
            foreground=Colors.TEXT_PRIMARY,
            borderwidth=0,
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold")
        )

        # Create Treeview
        self.tree = ttk.Treeview(
            self,
            columns=("columns", "rows"),
            show="tree headings",
            style="Custom.Treeview",
            height=15
        )

        # Columns
        self.tree.heading("#0", text="Table Name")
        self.tree.heading("columns", text="Columns")
        self.tree.heading("rows", text="Rows")

        self.tree.column("#0", width=200)
        self.tree.column("columns", width=80, anchor="center")
        self.tree.column("rows", width=100, anchor="right")

        # Scrollbar
        scrollbar = ctk.CTkScrollbar(self, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=(0, 20))
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=(0, 20))

        # Bind events
        self.tree.bind("<Double-1>", self.on_table_double_click)

    def load_tables(self, tables):
        """테이블 목록 로드"""
        self.tree.delete(*self.tree.get_children())

        for table in tables:
            self.tree.insert(
                "",
                "end",
                text=f"  {table['name']}",
                values=(table['columnCount'], f"{table['rowCount']:,}")
            )
```

#### 4. Excel Upload Dialog

```python
from tkinter import filedialog

class ExcelUploadDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Upload Excel to SQLite")
        self.geometry("600x500")

        # Main frame
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        title = ctk.CTkLabel(
            main,
            text="Upload Excel File",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold")
        )
        title.pack(pady=(0, 20))

        # File selection
        file_frame = ctk.CTkFrame(main, fg_color=Colors.BG_SECONDARY, corner_radius=Styles.CORNER_RADIUS)
        file_frame.pack(fill="x", pady=(0, 20))

        self.file_label = ctk.CTkLabel(
            file_frame,
            text="No file selected",
            text_color=Colors.TEXT_SECONDARY
        )
        self.file_label.pack(padx=20, pady=20)

        btn_select = ctk.CTkButton(
            file_frame,
            text="Browse Files",
            command=self.select_file,
            height=Styles.BUTTON_HEIGHT
        )
        btn_select.pack(padx=20, pady=(0, 20))

        # Table name
        ctk.CTkLabel(
            main,
            text="Table Name",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.table_name_entry = ctk.CTkEntry(
            main,
            height=Styles.INPUT_HEIGHT,
            corner_radius=Styles.CORNER_RADIUS
        )
        self.table_name_entry.pack(fill="x", pady=(0, 20))

        # Upload mode
        ctk.CTkLabel(
            main,
            text="Upload Mode",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.mode_var = tk.StringVar(value="replace")

        modes = [
            ("Replace entire table", "replace"),
            ("Append to existing data", "append"),
        ]

        for text, value in modes:
            ctk.CTkRadioButton(
                main,
                text=text,
                variable=self.mode_var,
                value=value
            ).pack(anchor="w", pady=2)

        # Progress bar (hidden initially)
        self.progress_frame = ctk.CTkFrame(main, fg_color="transparent")

        self.progress = ctk.CTkProgressBar(self.progress_frame)
        self.progress.pack(fill="x", pady=(20, 5))
        self.progress.set(0)

        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="",
            text_color=Colors.TEXT_SECONDARY
        )
        self.progress_label.pack()

        # Buttons
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(side="bottom", pady=(20, 0))

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=Colors.BG_TERTIARY,
            hover_color=Colors.BORDER,
            height=Styles.BUTTON_HEIGHT
        ).pack(side="left", padx=5)

        self.btn_upload = ctk.CTkButton(
            btn_frame,
            text="Upload",
            command=self.upload,
            fg_color=Colors.ACCENT,
            hover_color=Colors.ACCENT_HOVER,
            height=Styles.BUTTON_HEIGHT
        )
        self.btn_upload.pack(side="left", padx=5)
        self.btn_upload.configure(state="disabled")

    def select_file(self):
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.selected_file = filename
            self.file_label.configure(text=Path(filename).name)

            # Auto-fill table name
            table_name = Path(filename).stem.replace(" ", "_").lower()
            self.table_name_entry.delete(0, "end")
            self.table_name_entry.insert(0, table_name)

            self.btn_upload.configure(state="normal")

    def upload(self):
        """업로드 실행"""
        self.btn_upload.configure(state="disabled")
        self.progress_frame.pack(fill="x", pady=(20, 0))

        # Background thread로 업로드 (UI 블록 방지)
        import threading

        def upload_task():
            try:
                from core.excel_loader import ExcelLoader
                from core.db_manager import DatabaseManager

                # Load Excel
                self.update_progress(0.1, "Loading Excel file...")
                loader = ExcelLoader()
                df = loader.load_excel_file(Path(self.selected_file))

                # Upload
                self.update_progress(0.3, "Uploading to database...")
                db = DatabaseManager(self.master.current_db_path)

                table_name = self.table_name_entry.get()
                mode = self.mode_var.get()

                rows = db.dataframe_to_table(df, table_name, if_exists=mode)

                self.update_progress(1.0, f"Complete! {rows:,} rows uploaded")

                # Success
                self.after(1000, self.on_success)

            except Exception as e:
                self.after(0, lambda: self.on_error(str(e)))

        threading.Thread(target=upload_task, daemon=True).start()

    def update_progress(self, value, message):
        """진행률 업데이트 (스레드 안전)"""
        self.after(0, lambda: self.progress.set(value))
        self.after(0, lambda: self.progress_label.configure(text=message))
```

#### 5. Table Browser

```python
class TableBrowser(ctk.CTkToplevel):
    def __init__(self, parent, table_name, db_path):
        super().__init__(parent)

        self.table_name = table_name
        self.db_path = db_path
        self.current_page = 1
        self.page_size = 100

        self.title(f"Browse: {table_name}")
        self.geometry("1200x700")

        # Top bar
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(20, 10))

        # Title
        ctk.CTkLabel(
            top_bar,
            text=f"📊 {table_name}",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_XL, "bold")
        ).pack(side="left")

        # Search
        self.search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="Search...",
            width=300,
            height=Styles.INPUT_HEIGHT
        )
        self.search_entry.pack(side="right", padx=5)

        # Treeview
        self.tree_frame = ctk.CTkFrame(self, fg_color=Colors.BG_SECONDARY)
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Pagination
        pagination = ctk.CTkFrame(self, fg_color="transparent")
        pagination.pack(fill="x", padx=20, pady=(0, 20))

        self.page_label = ctk.CTkLabel(pagination, text="Page 1")
        self.page_label.pack(side="left")

        ctk.CTkButton(
            pagination,
            text="Previous",
            width=100,
            command=self.prev_page
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            pagination,
            text="Next",
            width=100,
            command=self.next_page
        ).pack(side="right")

        # Load data
        self.load_data()

    def load_data(self):
        """데이터 로드"""
        from core.db_manager import DatabaseManager

        db = DatabaseManager(self.db_path)
        conn = db.get_connection()
        cursor = conn.cursor()

        # Get columns
        cursor.execute(f"PRAGMA table_info({self.table_name})")
        columns = [row[1] for row in cursor.fetchall()]

        # Get data
        offset = (self.current_page - 1) * self.page_size
        cursor.execute(
            f"SELECT * FROM {self.table_name} LIMIT ? OFFSET ?",
            (self.page_size, offset)
        )
        rows = cursor.fetchall()

        # Create/update treeview
        if hasattr(self, 'tree'):
            self.tree.destroy()

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        for row in rows:
            self.tree.insert("", "end", values=row)

        # Scrollbars
        vsb = ctk.CTkScrollbar(self.tree_frame, command=self.tree.yview)
        hsb = ctk.CTkScrollbar(self.tree_frame, command=self.tree.xview, orientation="horizontal")

        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        self.tree_frame.grid_rowconfigure(0, weight=1)
        self.tree_frame.grid_columnconfigure(0, weight=1)
```

#### 6. Table Editor (Create/Modify)

```python
class TableEditorDialog(ctk.CTkToplevel):
    def __init__(self, parent, mode="create", table_name=None):
        super().__init__(parent)

        self.mode = mode  # "create" or "modify"
        self.columns = []

        title_text = "Create Table" if mode == "create" else f"Modify Table: {table_name}"
        self.title(title_text)
        self.geometry("800x600")

        # Main frame
        main = ctk.CTkScrollableFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Table name
        ctk.CTkLabel(
            main,
            text="Table Name",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.table_name_entry = ctk.CTkEntry(main, height=Styles.INPUT_HEIGHT)
        self.table_name_entry.pack(fill="x", pady=(0, 20))

        if table_name:
            self.table_name_entry.insert(0, table_name)
            self.table_name_entry.configure(state="disabled")

        # Columns section
        ctk.CTkLabel(
            main,
            text="Columns",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_LG, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.columns_frame = ctk.CTkFrame(main, fg_color="transparent")
        self.columns_frame.pack(fill="both", expand=True, pady=(0, 10))

        ctk.CTkButton(
            main,
            text="+ Add Column",
            command=self.add_column,
            fg_color=Colors.ACCENT,
            height=Styles.BUTTON_HEIGHT
        ).pack(fill="x", pady=(0, 20))

        # SQL Preview
        ctk.CTkLabel(
            main,
            text="SQL Preview",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_BASE, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.sql_preview = ctk.CTkTextbox(
            main,
            height=100,
            fg_color=Colors.BG_TERTIARY,
            font=("Consolas", 12)
        )
        self.sql_preview.pack(fill="x", pady=(0, 20))
        self.sql_preview.configure(state="disabled")

        # Buttons
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x")

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.destroy,
            fg_color=Colors.BG_TERTIARY,
            height=Styles.BUTTON_HEIGHT
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_frame,
            text="Create Table" if mode == "create" else "Apply Changes",
            command=self.save,
            fg_color=Colors.ACCENT,
            height=Styles.BUTTON_HEIGHT
        ).pack(side="left", padx=5)

        # Add first column
        self.add_column()

    def add_column(self):
        """컬럼 추가"""
        col_frame = ctk.CTkFrame(self.columns_frame, fg_color=Colors.BG_SECONDARY, corner_radius=Styles.CORNER_RADIUS)
        col_frame.pack(fill="x", pady=5)

        # Column name
        name_entry = ctk.CTkEntry(col_frame, placeholder_text="Column name", width=150)
        name_entry.grid(row=0, column=0, padx=10, pady=10)

        # Type
        type_var = tk.StringVar(value="TEXT")
        type_menu = ctk.CTkOptionMenu(
            col_frame,
            values=["INTEGER", "TEXT", "REAL", "DATE", "DATETIME"],
            variable=type_var,
            width=120
        )
        type_menu.grid(row=0, column=1, padx=10, pady=10)

        # Constraints
        pk_var = tk.BooleanVar()
        ctk.CTkCheckBox(col_frame, text="PK", variable=pk_var, width=60).grid(row=0, column=2, padx=5, pady=10)

        nn_var = tk.BooleanVar()
        ctk.CTkCheckBox(col_frame, text="NOT NULL", variable=nn_var, width=100).grid(row=0, column=3, padx=5, pady=10)

        unique_var = tk.BooleanVar()
        ctk.CTkCheckBox(col_frame, text="UNIQUE", variable=unique_var, width=100).grid(row=0, column=4, padx=5, pady=10)

        # Remove button
        ctk.CTkButton(
            col_frame,
            text="×",
            width=30,
            command=lambda: self.remove_column(col_frame),
            fg_color=Colors.ERROR
        ).grid(row=0, column=5, padx=10, pady=10)

        # Store reference
        col_frame.widgets = {
            'name': name_entry,
            'type': type_var,
            'pk': pk_var,
            'nn': nn_var,
            'unique': unique_var
        }

        self.columns.append(col_frame)
        self.update_sql_preview()

    def remove_column(self, col_frame):
        """컬럼 제거"""
        self.columns.remove(col_frame)
        col_frame.destroy()
        self.update_sql_preview()

    def update_sql_preview(self):
        """SQL 미리보기 업데이트"""
        table_name = self.table_name_entry.get() or "table_name"

        col_defs = []
        for col_frame in self.columns:
            w = col_frame.widgets
            name = w['name'].get() or "column_name"
            type_ = w['type'].get()

            col_def = f"{name} {type_}"
            if w['pk'].get():
                col_def += " PRIMARY KEY"
            if w['nn'].get():
                col_def += " NOT NULL"
            if w['unique'].get():
                col_def += " UNIQUE"

            col_defs.append(col_def)

        if col_defs:
            sql = f"CREATE TABLE {table_name} (\n  " + ",\n  ".join(col_defs) + "\n);"
        else:
            sql = "-- Add columns to see SQL preview"

        self.sql_preview.configure(state="normal")
        self.sql_preview.delete("1.0", "end")
        self.sql_preview.insert("1.0", sql)
        self.sql_preview.configure(state="disabled")
```

---

## 구현 단계별 계획

### 🚀 Phase 1: 프로젝트 셋업 및 기본 UI (Week 1)

#### Day 1-2: 환경 설정
- [ ] Python 가상환경 생성
- [ ] CustomTkinter 설치 및 테스트
- [ ] 프로젝트 폴더 구조 생성
- [ ] `ui/styles.py` 작성 (shadcn/ui 색상)

#### Day 3-4: 메인 윈도우
- [ ] `main.py` 작성
- [ ] `ui/main_window.py` 작성
- [ ] Sidebar 레이아웃
- [ ] Main Content 영역

#### Day 5-7: DB 선택/생성
- [ ] `ui/components/database_selector.py`
- [ ] 파일 다이얼로그 (열기/새로 만들기)
- [ ] DB 정보 카드
- [ ] 최근 DB 목록 (JSON 파일 저장)

**결과물**: 앱 실행 → DB 선택 → 정보 표시

---

### 📊 Phase 2: 테이블 관리 (Week 2)

#### Day 1-2: 테이블 목록
- [ ] `ui/components/table_list.py`
- [ ] Treeview 스타일링 (shadcn/ui)
- [ ] DB에서 테이블 목록 가져오기
- [ ] 테이블 통계 (컬럼 수, 행 수)

#### Day 3-5: 테이블 브라우저
- [ ] `ui/components/table_browser.py`
- [ ] 페이지네이션 (100행씩)
- [ ] 정렬 기능
- [ ] 검색 필터

#### Day 6-7: 테이블 생성/수정
- [ ] `ui/components/table_editor.py`
- [ ] 컬럼 추가/제거 UI
- [ ] SQL 미리보기
- [ ] DB에 CREATE TABLE 실행

**결과물**: 테이블 목록 → 브라우저 → 생성/수정

---

### 📤 Phase 3: Excel 업로드 (Week 3)

#### Day 1-3: 업로드 다이얼로그
- [ ] `ui/components/excel_uploader.py`
- [ ] 파일 선택 다이얼로그
- [ ] 테이블명 자동 입력
- [ ] 업로드 모드 선택 (Replace/Append)

#### Day 4-5: 업로드 실행
- [ ] 백그라운드 스레드로 업로드
- [ ] 진행률 바 업데이트
- [ ] 완료 후 테이블 목록 갱신
- [ ] 에러 처리

#### Day 6-7: 최적화 및 배포
- [ ] PyInstaller 설정
- [ ] 단일 exe 파일 생성
- [ ] 아이콘 추가
- [ ] 테스트 및 버그 수정

**결과물**: 완성된 앱 (30MB exe)

---

## 기술 스택 상세

### Python 라이브러리

```txt
# requirements.txt
customtkinter>=5.2.0      # 모던 UI 프레임워크
pandas>=2.0.0             # Excel 처리
openpyxl>=3.1.0           # Excel 파일 지원
Pillow>=10.0.0            # 이미지 처리 (CustomTkinter 의존성)
```

### 개발 도구

```txt
# requirements-dev.txt
pyinstaller>=6.0.0        # 실행 파일 빌드
black                     # 코드 포매터
```

### 배포

```bash
# 단일 실행 파일 생성
pyinstaller --onefile --windowed --icon=icon.ico main.py

# 결과: dist/main.exe (약 30MB)
```

---

## 프로젝트 구조

```
Excel-uploader/
├── main.py                         # 앱 진입점
│
├── ui/
│   ├── __init__.py
│   ├── main_window.py              # 메인 윈도우
│   ├── styles.py                   # shadcn/ui 색상 및 스타일
│   │
│   └── components/
│       ├── __init__.py
│       ├── database_selector.py    # DB 선택/생성 카드
│       ├── table_list.py           # 테이블 목록 (Treeview)
│       ├── table_browser.py        # 테이블 데이터 브라우저
│       ├── excel_uploader.py       # Excel 업로드 다이얼로그
│       └── table_editor.py         # 테이블 생성/수정 다이얼로그
│
├── core/
│   ├── __init__.py
│   ├── db_manager.py               ✅ 기존 (일부 수정)
│   └── excel_loader.py             ✅ 기존
│
├── assets/
│   └── icon.ico                    # 앱 아이콘
│
├── config/
│   └── recent_dbs.json             # 최근 DB 목록
│
├── requirements.txt                # 의존성
├── requirements-dev.txt            # 개발 의존성
├── build.bat                       # 빌드 스크립트
└── README.md
```

**총 코드 파일**: 약 10개
**예상 코드량**: 약 2,000줄 (Electron 대비 1/10)

---

## 예상 일정

| Week | 작업 | 주요 기능 |
|------|------|----------|
| **1주** | 셋업 + DB 관리 | 앱 실행, DB 선택/생성, 정보 표시 |
| **2주** | 테이블 관리 | 테이블 목록, 브라우저, 생성/수정 |
| **3주** | Excel 업로드 + 배포 | 업로드 기능, 최적화, exe 빌드 |

**총 소요 기간**: **3주** (Electron 대비 절반)

---

## 핵심 코드 미리보기

### `main.py`

```python
#!/usr/bin/env python3
"""
SQLite Manager - Main Entry Point
"""
import customtkinter as ctk
from ui.main_window import MainWindow

def main():
    # Set appearance
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    # Create and run app
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
```

### `ui/main_window.py` (핵심 부분)

```python
import customtkinter as ctk
from pathlib import Path
from ui.styles import Colors, Styles
from ui.components.database_selector import DatabaseSelector
from ui.components.table_list import TableList
from ui.components.excel_uploader import ExcelUploadDialog

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("SQLite Manager")
        self.geometry("1400x900")

        # Current DB
        self.current_db_path = None

        # Layout
        self.setup_ui()

    def setup_ui(self):
        # Grid configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = self.create_sidebar()
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        # Main content
        self.main_content = ctk.CTkFrame(self, fg_color="transparent")
        self.main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Database selector
        self.db_selector = DatabaseSelector(self.main_content, self.on_db_selected)
        self.db_selector.pack(fill="x", pady=(0, 20))

        # Table list
        self.table_list = TableList(self.main_content, self.on_table_selected)
        self.table_list.pack(fill="both", expand=True)

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=200, corner_radius=0, fg_color=Colors.BG_SECONDARY)

        # Logo/Title
        title = ctk.CTkLabel(
            sidebar,
            text="SQLite Manager",
            font=(Styles.FONT_FAMILY, Styles.FONT_SIZE_LG, "bold")
        )
        title.pack(padx=20, pady=(30, 40))

        # Buttons
        buttons = [
            ("📁 Open Database", self.open_database),
            ("➕ New Database", self.create_database),
            ("📤 Upload Excel", self.upload_excel),
        ]

        for text, command in buttons:
            btn = ctk.CTkButton(
                sidebar,
                text=text,
                command=command,
                height=Styles.BUTTON_HEIGHT,
                fg_color=Colors.BG_TERTIARY,
                hover_color=Colors.BORDER,
                anchor="w"
            )
            btn.pack(padx=20, pady=5, fill="x")

        return sidebar

    def open_database(self):
        from tkinter import filedialog

        filename = filedialog.askopenfilename(
            title="Select SQLite Database",
            filetypes=[("SQLite Database", "*.db"), ("All files", "*.*")]
        )

        if filename:
            self.on_db_selected(filename)

    def create_database(self):
        from tkinter import filedialog

        filename = filedialog.asksaveasfilename(
            title="Create New Database",
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")]
        )

        if filename:
            Path(filename).touch()
            self.on_db_selected(filename)

    def upload_excel(self):
        if not self.current_db_path:
            # Show error
            return

        dialog = ExcelUploadDialog(self)
        dialog.grab_set()

    def on_db_selected(self, db_path):
        self.current_db_path = db_path
        self.db_selector.load_database(db_path)
        self.table_list.load_tables(db_path)

    def on_table_selected(self, table_name):
        from ui.components.table_browser import TableBrowser

        browser = TableBrowser(self, table_name, self.current_db_path)
        browser.grab_set()
```

---

## 성능 목표

### 메모리 사용
- **목표**: 50-80MB
- **Electron 대비**: 4배 적음

### 시작 속도
- **목표**: 0.5초 이내
- **Electron 대비**: 6-10배 빠름

### 배포 크기
- **목표**: 30MB 단일 exe
- **Electron 대비**: 7배 작음

### 응답성
- **테이블 목록 로드**: 0.1초 이내 (1,000개 테이블 기준)
- **데이터 브라우저 렌더링**: 0.2초 이내 (100행 기준)
- **Excel 업로드**: 실시간 진행률 표시 (블록 없음)

---

## 다음 단계

### 즉시 시작 가능

1. **환경 설정** (5분)
   ```bash
   cd c:\Project\Excel-uploader
   python -m venv venv
   venv\Scripts\activate
   pip install customtkinter pandas openpyxl
   ```

2. **테스트 앱** (5분)
   ```python
   # test_app.py
   import customtkinter as ctk

   ctk.set_appearance_mode("dark")

   app = ctk.CTk()
   app.title("SQLite Manager")
   app.geometry("800x600")

   label = ctk.CTkLabel(app, text="SQLite Manager", font=("Segoe UI", 24, "bold"))
   label.pack(pady=50)

   button = ctk.CTkButton(app, text="Open Database", height=40, corner_radius=8)
   button.pack()

   app.mainloop()
   ```

3. **본격 개발 시작** (Week 1)

---

**시작할까요?** 🚀
