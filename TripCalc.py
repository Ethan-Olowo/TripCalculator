import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QCheckBox, QComboBox,
    QFrame, QScrollArea, QSizePolicy, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont, QColor, QPalette, QIcon

from trip_logic import load_activities, process_trip

base_dir = os.path.dirname(__file__)
ACTIVITIES_FILE = os.path.join(base_dir, "Activities.txt")

# ── Palette ────────────────────────────────────────────────────────────────────
BG          = "#0f0f0f"
SURFACE     = "#181818"
CARD        = "#1e1e1e"
BORDER      = "#2a2a2a"
BORDER_FOCUS= "#3a7bd5"
TEXT        = "#f0f0f0"
TEXT_MUTED  = "#888888"
ACCENT      = "#3a7bd5"
ACCENT_HOVER= "#4a8be5"
DANGER      = "#e05252"
SUCCESS     = "#3acca0"
INPUT_BG    = "#141414"


STYLESHEET = f"""
/* ── Root ── */
QMainWindow, QWidget#root {{
    background: {BG};
}}

/* ── Scroll area ── */
QScrollArea {{
    background: transparent;
    border: none;
}}
QScrollBar:vertical {{
    background: {SURFACE};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 24px;
}}
QScrollBar::handle:vertical:hover {{
    background: {TEXT_MUTED};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* ── Card ── */
QFrame#card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}

/* ── Section title ── */
QLabel#sectionTitle {{
    color: {TEXT_MUTED};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.4px;
}}

/* ── Labels ── */
QLabel#fieldLabel {{
    color: {TEXT};
    font-size: 13px;
    font-weight: 500;
}}

/* ── Text inputs ── */
QLineEdit, QTextEdit, QComboBox {{
    background: {INPUT_BG};
    border: 1px solid {BORDER};
    border-radius: 7px;
    color: {TEXT};
    font-size: 13px;
    padding: 8px 12px;
    selection-background-color: {ACCENT};
}}
QLineEdit:focus, QTextEdit:focus, QComboBox:focus {{
    border: 1px solid {BORDER_FOCUS};
}}
QLineEdit::placeholder, QTextEdit::placeholder {{
    color: {TEXT_MUTED};
}}

/* ── Combobox dropdown ── */
QComboBox::drop-down {{
    border: none;
    width: 28px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {TEXT_MUTED};
    margin-right: 8px;
}}
QComboBox QAbstractItemView {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 7px;
    color: {TEXT};
    selection-background-color: {ACCENT};
    outline: none;
    padding: 4px;
}}

/* ── Checkboxes ── */
QCheckBox {{
    color: {TEXT};
    font-size: 13px;
    spacing: 8px;
}}
QCheckBox::indicator {{
    width: 17px;
    height: 17px;
    border-radius: 5px;
    border: 1px solid {BORDER};
    background: {INPUT_BG};
}}
QCheckBox::indicator:checked {{
    background: {ACCENT};
    border: 1px solid {ACCENT};
    image: none;
}}
QCheckBox::indicator:hover {{
    border: 1px solid {ACCENT};
}}

/* ── Primary button ── */
QPushButton#primaryBtn {{
    background: {ACCENT};
    color: #ffffff;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    padding: 12px 24px;
    letter-spacing: 0.3px;
}}
QPushButton#primaryBtn:hover {{
    background: {ACCENT_HOVER};
}}
QPushButton#primaryBtn:pressed {{
    background: #2a6bc5;
}}
QPushButton#primaryBtn:disabled {{
    background: {BORDER};
    color: {TEXT_MUTED};
}}

/* ── Results box ── */
QFrame#resultsCard {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 10px;
}}
QLabel#resultsText {{
    color: {TEXT};
    font-size: 13px;
    line-height: 1.7;
}}
QLabel#resultsEmpty {{
    color: {TEXT_MUTED};
    font-size: 13px;
}}

/* ── Divider ── */
QFrame#divider {{
    background: {BORDER};
    max-height: 1px;
}}
"""


def make_card() -> QFrame:
    f = QFrame()
    f.setObjectName("card")
    return f


def section_title(text: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setObjectName("sectionTitle")
    return lbl


def field_label(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("fieldLabel")
    return lbl


class TripCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Trip Calculator")
        self.setMinimumSize(560, 700)
        self.resize(600, 760)
        self.setStyleSheet(STYLESHEET)

        try:
            self.setWindowIcon(QIcon(os.path.join(base_dir, "AppIcon.icns")))
        except Exception:
            pass

        self._build_ui()

    # ── UI construction ────────────────────────────────────────────────────────

    def _build_ui(self):
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Header ──
        header = self._make_header()
        outer.addWidget(header)

        # ── Scrollable body ──
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        body = QWidget()
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(24, 20, 24, 28)
        body_layout.setSpacing(16)

        body_layout.addWidget(self._make_activity_card())
        body_layout.addWidget(self._make_route_card())
        body_layout.addWidget(self._make_fuel_card())
        body_layout.addWidget(self._make_options_card())
        body_layout.addWidget(self._make_calculate_button())
        body_layout.addWidget(self._make_results_card())
        body_layout.addStretch()

        scroll.setWidget(body)
        outer.addWidget(scroll)

    def _make_header(self) -> QWidget:
        w = QWidget()
        w.setFixedHeight(64)
        w.setStyleSheet(f"background: {SURFACE}; border-bottom: 1px solid {BORDER};")

        layout = QHBoxLayout(w)
        layout.setContentsMargins(24, 0, 24, 0)

        title = QLabel("Trip Calculator")
        title.setStyleSheet(f"color: {TEXT}; font-size: 17px; font-weight: 700; background: transparent;")

        subtitle = QLabel("Fuel · Distance · Cost")
        subtitle.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 12px; background: transparent;")

        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(subtitle)
        return w

    def _make_activity_card(self) -> QFrame:
        card = make_card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Activity"))

        lbl = field_label("Select or type an activity name")
        layout.addWidget(lbl)

        activities = load_activities()
        self.activity_combo = QComboBox()
        self.activity_combo.setEditable(True)
        self.activity_combo.addItems(list(activities.keys()))
        self.activity_combo.setPlaceholderText("e.g. Client Visit")
        self.activity_combo.setFixedHeight(38)
        layout.addWidget(self.activity_combo)

        return card

    def _make_route_card(self) -> QFrame:
        card = make_card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Route"))

        layout.addWidget(field_label("Origin"))
        self.origin_entry = QLineEdit()
        self.origin_entry.setPlaceholderText("e.g. Kampala, Uganda")
        self.origin_entry.setFixedHeight(38)
        layout.addWidget(self.origin_entry)

        layout.addSpacing(4)
        layout.addWidget(field_label("Stops"))
        hint = QLabel("One location per line")
        hint.setStyleSheet(f"color: {TEXT_MUTED}; font-size: 11px;")
        layout.addWidget(hint)
        self.stops_text = QTextEdit()
        self.stops_text.setPlaceholderText("Kampala\nNairobi\nDar es Salaam")
        self.stops_text.setFixedHeight(100)
        layout.addWidget(self.stops_text)

        return card

    def _make_fuel_card(self) -> QFrame:
        card = make_card()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(10)

        layout.addWidget(section_title("Fuel"))

        row = QHBoxLayout()
        row.setSpacing(12)

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

    def _make_options_card(self) -> QFrame:
        card = make_card()
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

    def _make_calculate_button(self) -> QPushButton:
        btn = QPushButton("Calculate Trip")
        btn.setObjectName("primaryBtn")
        btn.setFixedHeight(46)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.clicked.connect(self._calculate_trip)
        self.calc_btn = btn
        return btn

    def _make_results_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("resultsCard")
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 16, 18, 18)
        layout.setSpacing(8)

        hdr = QHBoxLayout()
        hdr.addWidget(section_title("Results"))
        hdr.addStretch()
        layout.addLayout(hdr)

        divider = QFrame()
        divider.setObjectName("divider")
        divider.setFixedHeight(1)
        layout.addWidget(divider)

        self.results_label = QLabel("Run a calculation to see results here.")
        self.results_label.setObjectName("resultsEmpty")
        self.results_label.setWordWrap(True)
        self.results_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.results_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(self.results_label)

        return card

    # ── Logic ──────────────────────────────────────────────────────────────────

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

            if register_activity and not activity_name:
                raise ValueError("Please provide an activity name.")

            def file_dialog_func():
                path, _ = QFileDialog.getSaveFileName(
                    self, "Save Excel File", "", "Excel Files (*.xlsx)"
                )
                return path

            self.calc_btn.setEnabled(False)
            self.calc_btn.setText("Calculating…")
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
            )

            self.results_label.setObjectName("resultsText")
            self.results_label.setStyleSheet(
                f"color: {TEXT}; font-size: 13px; line-height: 1.8;"
            )
            self.results_label.setText(str(results))

        except ValueError as e:
            QMessageBox.warning(self, "Input Error", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            self.calc_btn.setEnabled(True)
            self.calc_btn.setText("Calculate Trip")


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Dark palette baseline so native widgets pick up dark colours
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(BG))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(TEXT))
    palette.setColor(QPalette.ColorRole.Base, QColor(INPUT_BG))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(SURFACE))
    palette.setColor(QPalette.ColorRole.Text, QColor(TEXT))
    palette.setColor(QPalette.ColorRole.Button, QColor(CARD))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(TEXT))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(ACCENT))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    win = TripCalculator()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()