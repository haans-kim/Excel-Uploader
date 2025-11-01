"""
UI Styles - shadcn/ui inspired design system
"""


class Colors:
    """Color palette based on shadcn/ui zinc theme (light/dark mode)"""

    # Background colors (light, dark)
    BG_PRIMARY = ("#f4f4f5", "#09090b")      # zinc-100, zinc-950
    BG_SECONDARY = ("#e4e4e7", "#18181b")    # zinc-200, zinc-900
    BG_TERTIARY = ("#d4d4d8", "#27272a")     # zinc-300, zinc-800
    BG_MUTED = ("#a1a1aa", "#3f3f46")        # zinc-400, zinc-700

    # Border colors (light, dark)
    BORDER = ("#d4d4d8", "#3f3f46")          # zinc-300, zinc-700
    BORDER_LIGHT = ("#e4e4e7", "#52525b")    # zinc-200, zinc-600

    # Text colors (light, dark) - 라이트 모드에서는 어두운 텍스트
    TEXT_PRIMARY = ("#09090b", "#fafafa")    # zinc-950, zinc-50
    TEXT_SECONDARY = ("#52525b", "#a1a1aa")  # zinc-600, zinc-400
    TEXT_MUTED = ("#71717a", "#71717a")      # zinc-500, zinc-500

    # Accent colors (blue) - 양쪽 모두 navy blue 사용
    ACCENT = ("#1e3a8a", "#3b82f6")          # navy, blue-500
    ACCENT_HOVER = ("#1e40af", "#2563eb")    # navy-light, blue-600
    ACCENT_LIGHT = ("#3b82f6", "#60a5fa")    # blue-500, blue-400

    # Status colors
    SUCCESS = "#22c55e"         # green-500
    SUCCESS_HOVER = "#16a34a"   # green-600

    ERROR = "#ef4444"           # red-500
    ERROR_HOVER = "#dc2626"     # red-600

    WARNING = "#f59e0b"         # amber-500
    WARNING_HOVER = "#d97706"   # amber-600

    INFO = "#0ea5e9"            # sky-500
    INFO_HOVER = "#0284c7"      # sky-600


class Styles:
    """Component styles and dimensions"""

    # Border radius
    CORNER_RADIUS = 8
    CORNER_RADIUS_SM = 6
    CORNER_RADIUS_LG = 12

    # Border width
    BORDER_WIDTH = 1
    BORDER_WIDTH_THICK = 2

    # Component heights
    BUTTON_HEIGHT = 40
    BUTTON_HEIGHT_SM = 32
    BUTTON_HEIGHT_LG = 48

    INPUT_HEIGHT = 40
    INPUT_HEIGHT_SM = 32

    # Spacing
    PADDING_SM = 10
    PADDING = 20
    PADDING_LG = 30

    # Typography
    FONT_FAMILY = "Segoe UI"
    FONT_FAMILY_MONO = "Consolas"

    FONT_SIZE_XS = 11
    FONT_SIZE_SM = 12
    FONT_SIZE_BASE = 14
    FONT_SIZE_LG = 16
    FONT_SIZE_XL = 20
    FONT_SIZE_2XL = 24

    # Sidebar
    SIDEBAR_WIDTH = 200

    # Animation
    HOVER_TRANSITION = 200  # ms
