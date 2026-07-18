import html
import os
import sys

from PySide6.QtCore import QSettings, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QFileDialog,
    QScrollArea,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QStackedWidget,
)

from planner_page import build_planner_page
from settings_page import build_settings_page
from trip_logic import load_activities, process_trip
from trip_logic import load_activity_trip_defaults

base_dir = os.path.dirname(__file__)

THEMES = {
    "dark": {
        "bg": "#0f1114",
        "surface": "#171b22",
        "card": "#1e232b",
        "border": "#2e3643",
        "border_focus": "#18b8a0",
        "text": "#f4f7fb",
        "text_muted": "#95a1b5",
        "accent": "#18b8a0",
        "accent_hover": "#22ccb2",
        "danger": "#e86161",
        "success": "#2cc598",
        "input_bg": "#12161d",
        "metric_bg": "#151a22",
        "hero": "#0f1822",
    },
    "light": {
        "bg": "#f7f6f1",
        "surface": "#ece8dc",
        "card": "#fffdf7",
        "border": "#d9cfb5",
        "border_focus": "#0f8f7b",
        "text": "#2a1f16",
        "text_muted": "#7c6858",
        "accent": "#0f8f7b",
        "accent_hover": "#12a58f",
        "danger": "#c53e3e",
        "success": "#1d8e6c",
        "input_bg": "#f3ecdb",
        "metric_bg": "#f5eedf",
        "hero": "#f1e6cb",
    },
}


def build_stylesheet(colors):
    return f"""
QMainWindow, QWidget#root {{
    background: {colors['bg']};
}}

QWidget#mainPageBody, QWidget#settingsPageBody {{
    background: {colors['bg']};
}}

QWidget#header {{
    background: {colors['surface']};
    border-bottom: 1px solid {colors['border']};
}}

QLabel#title {{
    color: {colors['text']};
    font-size: 18px;
    font-weight: 700;
}}

QLabel#subtitle {{
    color: {colors['text_muted']};
    font-size: 12px;
}}

QToolButton#navIconBtn {{
    background: transparent;
    color: {colors['text_muted']};
    border: 1px solid {colors['border']};
    border-radius: 14px;
    padding: 0px;
}}

QToolButton#themeToggleBtn {{
    background: transparent;
    border: 1px solid {colors['border']};
    border-radius: 14px;
    padding: 0px;
}}
QToolButton#themeToggleBtn:hover {{
    border: 1px solid {colors['accent']};
}}
QToolButton#navIconBtn:hover {{
    color: {colors['text']};
    border: 1px solid {colors['accent']};
}}
QToolButton#navIconBtn[active="true"] {{
    background: {colors['accent']};
    color: #ffffff;
    border: 1px solid {colors['accent']};
}}

QLabel#formHint {{
    color: {colors['text_muted']};
    font-size: 12px;
}}

QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background: {colors['surface']};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {colors['border']};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QFrame#card {{
    background: {colors['card']};
    border: 1px solid {colors['border']};
    border-radius: 12px;
}}

QFrame#heroCard {{
    background: {colors['hero']};
    border: 1px solid {colors['border']};
    border-radius: 12px;
}}

QLabel#sectionTitle {{
    color: {colors['text_muted']};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.2px;
}}

QLabel#fieldLabel {{
    color: {colors['text']};
    font-size: 13px;
    font-weight: 600;
}}

QLineEdit, QTextEdit, QComboBox {{
    background: {colors['input_bg']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    color: {colors['text']};
    font-size: 13px;
    padding: 8px 12px;
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 1px solid {colors['border_focus']};
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {colors['text_muted']};
}}

QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {colors['text_muted']};
    margin-right: 8px;
}}

QCheckBox {{
    color: {colors['text']};
    font-size: 13px;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 17px;
    height: 17px;
    border-radius: 5px;
    border: 1px solid {colors['border']};
    background: {colors['input_bg']};
}}
QCheckBox::indicator:checked {{
    background: {colors['accent']};
    border: 1px solid {colors['accent']};
}}

QPushButton#primaryBtn {{
    background: {colors['accent']};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 700;
    padding: 12px 24px;
}}
QPushButton#primaryBtn:hover {{
    background: {colors['accent_hover']};
}}
QPushButton#primaryBtn:disabled {{
    background: {colors['border']};
    color: {colors['text_muted']};
}}

QPushButton#ghostBtn {{
    background: transparent;
    color: {colors['text']};
    border: 1px solid {colors['border']};
    border-radius: 8px;
    font-size: 12px;
    font-weight: 600;
    padding: 8px 14px;
}}
QPushButton#ghostBtn:hover {{
    border: 1px solid {colors['accent']};
    color: {colors['accent']};
}}

QLabel#statusBadge {{
    color: {colors['success']};
    background: transparent;
    font-size: 12px;
    font-weight: 700;
}}
QLabel#statusBadge[error="true"] {{
    color: {colors['danger']};
}}

QFrame#metricCard {{
    background: {colors['metric_bg']};
    border: 1px solid {colors['border']};
    border-radius: 10px;
}}
QLabel#metricTitle {{
    color: {colors['text_muted']};
    font-size: 10px;
    letter-spacing: 1px;
    font-weight: 700;
}}
QLabel#metricValue {{
    color: {colors['text']};
    font-size: 20px;
    font-weight: 700;
}}

QLabel#resultsBody {{
    color: {colors['text']};
    font-size: 13px;
    line-height: 1.55;
}}
QLabel#errorBox {{
    color: {colors['danger']};
    background: transparent;
    border: 1px solid {colors['danger']};
    border-radius: 8px;
    padding: 10px;
    font-size: 12px;
}}

QLabel#infoTitle {{
    color: {colors['text']};
    font-size: 14px;
    font-weight: 700;
}}
QLabel#infoBody {{
    color: {colors['text_muted']};
    font-size: 13px;
    line-height: 1.6;
}}

QLabel#linkLabel {{
    color: {colors['accent']};
    font-size: 13px;
    font-weight: 600;
}}
"""


def make_card(name="card"):
    frame = QFrame()
    frame.setObjectName(name)
    return frame


def section_title(text):
    label = QLabel(text.upper())
    label.setObjectName("sectionTitle")
    return label


def field_label(text):
    label = QLabel(text)
    label.setObjectName("fieldLabel")
    return label


def make_metric_card(title):
    card = make_card("metricCard")
    layout = QVBoxLayout(card)
    layout.setContentsMargins(12, 10, 12, 10)
    layout.setSpacing(2)

    title_label = QLabel(title)
    title_label.setObjectName("metricTitle")

    value_label = QLabel("--")
    value_label.setObjectName("metricValue")

    layout.addWidget(title_label)
    layout.addWidget(value_label)
    return card, value_label


class TripCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("TripCalc", "TripCalculator")
        self.current_theme = self.settings.value("theme", "dark")
        if self.current_theme not in THEMES:
            self.current_theme = "dark"

        self.setWindowTitle("Trip Calculator")
        self.setMinimumSize(740, 760)
        self.resize(860, 840)

        self.icons_dir = os.path.join(base_dir, "icons")
        self.home_icon_path = os.path.join(self.icons_dir, "home-1-svgrepo-com.svg")
        self.settings_icon_path = os.path.join(self.icons_dir, "settings-svgrepo-com.svg")
        self.sun_icon_path = os.path.join(self.icons_dir, "sun-2-svgrepo-com.svg")
        self.moon_icon_path = os.path.join(self.icons_dir, "moon-svgrepo-com.svg")

        try:
            self.setWindowIcon(QIcon(os.path.join(self.icons_dir, "AppIcon.icns")))
        except Exception:
            pass

        self._build_ui()
        self._apply_theme(self.current_theme)
        self._load_saved_settings()

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        outer.addWidget(self._make_header())

        self.pages = QStackedWidget()
        self.pages.addWidget(self._make_main_page())
        self.pages.addWidget(self._make_settings_page())
        outer.addWidget(self.pages)

        self._switch_page(0)

    def _make_header(self):
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(58)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(14, 0, 14, 0)
        layout.setSpacing(6)

        title_col = QVBoxLayout()
        title_col.setContentsMargins(0, 0, 0, 0)
        title_col.setSpacing(1)

        title = QLabel("Trip Calculator")
        title.setObjectName("title")

        subtitle = QLabel("Plan cleaner routes with better fuel cost visibility")
        subtitle.setObjectName("subtitle")
        title.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        title_col.addStretch(1)
        title_col.addWidget(title)
        title_col.addWidget(subtitle)
        title_col.addStretch(1)

        self.main_nav_btn = QToolButton()
        self.main_nav_btn.setObjectName("navIconBtn")
        self.main_nav_btn.setFixedSize(30, 30)
        self.main_nav_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.main_nav_btn.setToolTip("Home")
        self.main_nav_btn.clicked.connect(lambda: self._switch_page(0))

        self.settings_nav_btn = QToolButton()
        self.settings_nav_btn.setObjectName("navIconBtn")
        self.settings_nav_btn.setFixedSize(30, 30)
        self.settings_nav_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.settings_nav_btn.setToolTip("Settings")
        self.settings_nav_btn.clicked.connect(lambda: self._switch_page(1))

        self.theme_toggle_btn = QToolButton()
        self.theme_toggle_btn.setObjectName("themeToggleBtn")
        self.theme_toggle_btn.setFixedSize(30, 30)
        self.theme_toggle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.theme_toggle_btn.setToolTip("Toggle theme")
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)

        left_slot = QWidget()
        left_slot.setFixedWidth(66)
        left_layout = QHBoxLayout(left_slot)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(4)
        left_layout.addWidget(self.main_nav_btn)
        left_layout.addStretch()

        right_slot = QWidget()
        right_slot.setFixedWidth(66)
        right_layout = QHBoxLayout(right_slot)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(4)
        right_layout.addStretch()
        right_layout.addWidget(self.theme_toggle_btn)
        right_layout.addWidget(self.settings_nav_btn)

        layout.addWidget(left_slot)
        layout.addStretch()
        layout.addLayout(title_col)
        layout.addStretch()
        layout.addWidget(right_slot)
        return header

    def _tinted_icon(self, icon_path, color_hex, size):
        icon = QIcon(icon_path)

        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)

        # Render SVG to fill the entire icon area
        icon.paint(
            painter,
            0,
            0,
            size,
            size,
            Qt.AlignmentFlag.AlignCenter,
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )

        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), QColor(color_hex))
        painter.end()

        return QIcon(pixmap)

    def _refresh_header_icons(self):
        colors = THEMES[self.current_theme]
        icon_color = colors["text"]
        home_size = int(min(self.main_nav_btn.width(), self.main_nav_btn.height()) * 0.6)
        settings_size = int(min(self.settings_nav_btn.width(), self.settings_nav_btn.height()) * 0.6)

        self.main_nav_btn.setIconSize(QSize(home_size, home_size))
        self.settings_nav_btn.setIconSize(QSize(settings_size, settings_size))
        self.main_nav_btn.setIcon(self._tinted_icon(self.home_icon_path, icon_color, size=home_size))
        self.settings_nav_btn.setIcon(self._tinted_icon(self.settings_icon_path, icon_color, size=settings_size))

    def _make_main_page(self):
        return build_planner_page(self)

    def _make_settings_page(self):
        return build_settings_page(self)

    def _make_activity_card(self):
        card = make_card("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Activity"))
        layout.addWidget(field_label("Select or type an activity name"))

        activities = load_activities()
        row = QHBoxLayout()
        row.setSpacing(8)

        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(list(activities.keys()))
        self.activity_combo.setPlaceholderText("e.g. Client Visit")
        self.activity_combo.setFixedHeight(38)
        self.activity_combo.activated.connect(lambda _: self._load_activity(auto=True))

        self.load_activity_btn = QPushButton("Load Activity")
        self.load_activity_btn.setObjectName("ghostBtn")
        self.load_activity_btn.setFixedHeight(38)
        self.load_activity_btn.clicked.connect(self._load_activity)

        row.addWidget(self.activity_combo)
        row.addWidget(self.load_activity_btn)
        layout.addLayout(row)

        self.activity_hint = QLabel("Pick an existing activity to restore saved route and fuel details.")
        self.activity_hint.setObjectName("formHint")
        layout.addWidget(self.activity_hint)

        return card

    def _make_route_card(self):
        card = make_card("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Route"))

        layout.addWidget(field_label("Origin"))
        self.origin_entry = QLineEdit()
        self.origin_entry.setPlaceholderText("e.g. Kampala, Uganda")
        self.origin_entry.setFixedHeight(38)
        layout.addWidget(self.origin_entry)

        layout.addWidget(field_label("Stops"))
        hint = QLabel("One location per line")
        hint.setObjectName("infoBody")
        layout.addWidget(hint)

        self.stops_text = QTextEdit()
        self.stops_text.setPlaceholderText("Kampala\nNairobi\nDar es Salaam")
        self.stops_text.setFixedHeight(120)
        layout.addWidget(self.stops_text)

        return card

    def _make_fuel_card(self):
        card = make_card("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Fuel"))

        row = QHBoxLayout()
        row.setSpacing(10)

        left = QVBoxLayout()
        left.setSpacing(6)
        left.addWidget(field_label("Efficiency (km/L)"))
        self.fuel_eff_entry = QLineEdit()
        self.fuel_eff_entry.setPlaceholderText("e.g. 12.0")
        self.fuel_eff_entry.setFixedHeight(38)
        left.addWidget(self.fuel_eff_entry)

        right = QVBoxLayout()
        right.setSpacing(6)
        right.addWidget(field_label("Price per Litre"))
        self.fuel_price_entry = QLineEdit()
        self.fuel_price_entry.setPlaceholderText("e.g. 1000")
        self.fuel_price_entry.setFixedHeight(38)
        right.addWidget(self.fuel_price_entry)

        row.addLayout(left)
        row.addLayout(right)
        layout.addLayout(row)

        return card

    def _make_options_card(self):
        card = make_card("card")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(12)

        layout.addWidget(section_title("Options"))

        self.round_trip_cb = QCheckBox("Round Trip")
        self.round_trip_cb.setChecked(True)

        self.save_excel_cb = QCheckBox("Save to Excel")
        self.save_excel_cb.setChecked(True)

        self.register_cb = QCheckBox("Register Activity")
        self.register_cb.setChecked(True)

        layout.addWidget(self.round_trip_cb)
        layout.addWidget(self.save_excel_cb)
        layout.addWidget(self.register_cb)

        return card

    def _make_calculate_button(self):
        btn = QPushButton("Calculate Trip")
        btn.setObjectName("primaryBtn")
        btn.setFixedHeight(46)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._calculate_trip)
        self.calc_btn = btn
        return btn

    def _make_results_card(self):
        card = make_card("heroCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        top = QHBoxLayout()
        top.addWidget(section_title("Results"))
        top.addStretch()

        self.status_badge = QLabel("IDLE")
        self.status_badge.setObjectName("statusBadge")
        self.status_badge.setProperty("error", "false")
        top.addWidget(self.status_badge)

        layout.addLayout(top)

        metrics = QHBoxLayout()
        metrics.setSpacing(8)
        distance_card, self.distance_value = make_metric_card("TOTAL DISTANCE")
        fuel_card, self.fuel_value = make_metric_card("TOTAL FUEL")
        cost_card, self.cost_value = make_metric_card("TOTAL COST")
        metrics.addWidget(distance_card)
        metrics.addWidget(fuel_card)
        metrics.addWidget(cost_card)
        layout.addLayout(metrics)

        self.error_box = QLabel("")
        self.error_box.setObjectName("errorBox")
        self.error_box.setWordWrap(True)
        self.error_box.hide()
        layout.addWidget(self.error_box)

        self.results_body = QLabel("Run a calculation to see route details and totals.")
        self.results_body.setObjectName("resultsBody")
        self.results_body.setWordWrap(True)
        self.results_body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.results_body.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.results_body)

        return card

    def _switch_page(self, index):
        self.pages.setCurrentIndex(index)
        self.main_nav_btn.setProperty("active", "true" if index == 0 else "false")
        self.settings_nav_btn.setProperty("active", "true" if index == 1 else "false")
        self.main_nav_btn.style().unpolish(self.main_nav_btn)
        self.main_nav_btn.style().polish(self.main_nav_btn)
        self.settings_nav_btn.style().unpolish(self.settings_nav_btn)
        self.settings_nav_btn.style().polish(self.settings_nav_btn)

    def _toggle_theme(self):
        theme = "light" if self.current_theme == "dark" else "dark"
        self.settings.setValue("theme", theme)
        self._apply_theme(theme)

    def _refresh_theme_toggle_icon(self):
        # Show the mode user can switch to: sun for light mode, moon for dark mode.
        colors = THEMES[self.current_theme]
        icon_color = colors["text"]
        theme_size = int(min(
            self.theme_toggle_btn.width(),
            self.theme_toggle_btn.height()
        ) * 0.6)
        self.theme_toggle_btn.setIconSize(QSize(theme_size, theme_size))
        if self.current_theme == "dark":
            self.theme_toggle_btn.setIcon(self._tinted_icon(self.sun_icon_path, icon_color, size=theme_size))
            self.theme_toggle_btn.setToolTip("Switch to light mode")
        else:
            self.theme_toggle_btn.setIcon(self._tinted_icon(self.moon_icon_path, icon_color, size=theme_size))
            self.theme_toggle_btn.setToolTip("Switch to dark mode")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Keep toolbar icons at 80% of button size after any window scaling.
        self._refresh_header_icons()
        self._refresh_theme_toggle_icon()

    def _apply_theme(self, theme):
        self.current_theme = theme
        colors = THEMES[theme]
        self.setStyleSheet(build_stylesheet(colors))
        self._refresh_header_icons()
        self._refresh_theme_toggle_icon()

        app = QApplication.instance()
        if app is not None:
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["bg"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["input_bg"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["card"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["accent"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
            app.setPalette(palette)

    def _toggle_key_visibility(self, checked):
        if checked:
            self.api_key_entry.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.api_key_entry.setEchoMode(QLineEdit.EchoMode.Password)

    def _save_settings(self):
        key = self.api_key_entry.text().strip()
        self.settings.setValue("ors_api_key", key)
        self.settings.sync()

        if key:
            self.settings_status.setText("API key saved locally for this app profile.")
        else:
            self.settings_status.setText("API key removed.")

        self._update_submit_state()

    def _clear_api_key(self):
        self.api_key_entry.clear()
        self._save_settings()

    def _load_saved_settings(self):
        saved_key = self.settings.value("ors_api_key", "")
        self.api_key_entry.setText(saved_key)

        saved_theme = self.settings.value("theme", self.current_theme)
        self._apply_theme(saved_theme)

        self._wire_validation()
        self._update_submit_state()

    def _wire_validation(self):
        self.origin_entry.textChanged.connect(self._update_submit_state)
        self.stops_text.textChanged.connect(self._update_submit_state)
        self.fuel_eff_entry.textChanged.connect(self._update_submit_state)
        self.fuel_price_entry.textChanged.connect(self._update_submit_state)
        self.activity_combo.currentTextChanged.connect(self._update_submit_state)
        self.register_cb.toggled.connect(self._update_submit_state)
        self.api_key_entry.textChanged.connect(self._update_submit_state)

    def _try_parse_float(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _is_form_valid(self):
        origin = self.origin_entry.text().strip()
        stops = [s.strip() for s in self.stops_text.toPlainText().splitlines() if s.strip()]
        fuel_eff = self._try_parse_float(self.fuel_eff_entry.text().strip())
        fuel_price = self._try_parse_float(self.fuel_price_entry.text().strip())
        activity_name = self.activity_combo.currentText().strip()
        api_key = self.api_key_entry.text().strip()

        if not origin or not stops:
            return False
        if fuel_eff is None or fuel_eff <= 0:
            return False
        if fuel_price is None or fuel_price < 0:
            return False
        if self.register_cb.isChecked() and not activity_name:
            return False
        if not api_key:
            return False
        return True

    def _update_submit_state(self):
        self.calc_btn.setEnabled(self._is_form_valid())

    def _load_activity(self, auto=False):
        activity_name = self.activity_combo.currentText().strip()
        if not activity_name:
            if not auto:
                self._set_error_state("Select an activity to load.")
            return

        try:
            loaded = load_activity_trip_defaults(activity_name)
        except Exception as exc:
            self._set_error_state(str(exc))
            return

        self.origin_entry.setText(loaded["origin"])
        self.stops_text.setPlainText("\n".join(loaded["stops"]))
        self.fuel_eff_entry.setText(str(loaded["fuel_efficiency"]))
        self.fuel_price_entry.setText(str(loaded["fuel_price"]))
        self.round_trip_cb.setChecked(bool(loaded["round_trip"]))
        self.register_cb.setChecked(True)

        self.status_badge.setText("READY")
        self.status_badge.setProperty("error", "false")
        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)
        self.error_box.hide()
        self.results_body.setText(
            f"Loaded activity '{html.escape(activity_name)}' from {html.escape(loaded['file_path'])}."
        )
        self._update_submit_state()

    def _format_results_html(self, data):
        lines = []
        for leg in data["legs"]:
            lines.append(
                (
                    f"<b>{html.escape(leg['label'])}</b>: "
                    f"{html.escape(leg['from'])} -> {html.escape(leg['to'])}<br>"
                    f"Distance: {leg['distance']:.2f} km | "
                    f"Fuel: {leg['fuel']:.2f} L | "
                    f"Cost: {leg['cost']:.2f}"
                )
            )

        intro = (
            f"<b>Activity:</b> {html.escape(data['activity_name'] or '(not registered)')}<br>"
            f"<b>Route:</b> {html.escape(data['origin'])} to {html.escape(data['destination'])}"
        )

        return intro + "<br><br>" + "<br><br>".join(lines)

    def _set_metrics(self, distance=None, fuel=None, cost=None):
        self.distance_value.setText("--" if distance is None else f"{distance:.1f} km")
        self.fuel_value.setText("--" if fuel is None else f"{fuel:.1f} L")
        self.cost_value.setText("--" if cost is None else f"{cost:.2f}")

    def _set_error_state(self, details):
        self.status_badge.setText("ERROR")
        self.status_badge.setProperty("error", "true")
        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)

        self._set_metrics()
        self.error_box.setText(html.escape(details))
        self.error_box.show()
        self.results_body.setText("Fix the issue and run the calculation again.")

    def _set_success_state(self, data):
        self.status_badge.setText("READY")
        self.status_badge.setProperty("error", "false")
        self.status_badge.style().unpolish(self.status_badge)
        self.status_badge.style().polish(self.status_badge)

        self._set_metrics(data["total_distance"], data["total_fuel"], data["total_cost"])
        self.error_box.hide()
        self.results_body.setText(self._format_results_html(data))

    def _calculate_trip(self):
        try:
            origin = self.origin_entry.text().strip()
            stops_raw = self.stops_text.toPlainText().splitlines()
            stops = [s.strip() for s in stops_raw if s.strip()]
            fuel_eff = float(self.fuel_eff_entry.text().strip())
            fuel_price = float(self.fuel_price_entry.text().strip())
            round_trip = self.round_trip_cb.isChecked()
            save_to_excel = self.save_excel_cb.isChecked()
            register_activity = self.register_cb.isChecked()
            activity_name = self.activity_combo.currentText().strip()
            api_key = self.api_key_entry.text().strip()

            if register_activity and not activity_name:
                raise ValueError("Please provide an activity name.")

            if not api_key:
                raise ValueError("API key is missing. Add it in Settings.")

            def file_dialog_func():
                path, _ = QFileDialog.getSaveFileName(
                    self,
                    "Save Excel File",
                    "",
                    "Excel Files (*.xlsx)",
                )
                return path

            self.calc_btn.setEnabled(False)
            self.calc_btn.setText("Calculating...")
            QApplication.processEvents()

            results = process_trip(
                activity_name=activity_name,
                origin=origin,
                stops=stops,
                fuel_efficiency=fuel_eff,
                fuel_price=fuel_price,
                round_trip=round_trip,
                file_dialog_func=file_dialog_func,
                save_to_excel=save_to_excel,
                register_activity=register_activity,
                api_key=api_key,
            )

            self._set_success_state(results)

        except ValueError as exc:
            self._set_error_state(str(exc))
        except Exception as exc:
            self._set_error_state(str(exc))
            QMessageBox.critical(self, "Trip Calculation Failed", str(exc))
        finally:
            self.calc_btn.setEnabled(True)
            self.calc_btn.setText("Calculate Trip")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    win = TripCalculator()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
