from PySide6.QtCore import Qt
from PySide6.QtWidgets import QCheckBox, QFrame, QHBoxLayout, QLabel, QLineEdit, QPushButton, QScrollArea, QVBoxLayout, QWidget


def _make_card(name="card"):
    frame = QFrame()
    frame.setObjectName(name)
    return frame


def _section_title(text):
    label = QLabel(text.upper())
    label.setObjectName("sectionTitle")
    return label


def _field_label(text):
    label = QLabel(text)
    label.setObjectName("fieldLabel")
    return label


def build_settings_page(window):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    body = QWidget()
    body.setObjectName("settingsPageBody")
    layout = QVBoxLayout(body)
    layout.setContentsMargins(24, 20, 24, 28)
    layout.setSpacing(14)

    api_card = _make_card("card")
    api_layout = QVBoxLayout(api_card)
    api_layout.setContentsMargins(18, 16, 18, 18)
    api_layout.setSpacing(10)

    api_layout.addWidget(_section_title("API Settings"))
    api_layout.addWidget(_field_label("OpenRouteService API Key"))

    window.api_key_entry = QLineEdit()
    window.api_key_entry.setPlaceholderText("Enter your ORS API key")
    window.api_key_entry.setEchoMode(QLineEdit.EchoMode.Password)
    window.api_key_entry.setFixedHeight(38)
    api_layout.addWidget(window.api_key_entry)

    api_help = QLabel(
        "How to get an API key:\n"
        "1. Create an account on OpenRouteService (heiGIT).\n"
        "2. Open the Dashboard and create a new token.\n"
        "3. Copy the key and paste it above.\n"
        "4. Click Save API Key."
    )
    api_help.setObjectName("infoBody")
    api_help.setWordWrap(True)
    api_layout.addWidget(api_help)

    api_docs_link = QLabel(
        '<a href="https://openrouteservice.org/dev/#/signup">openrouteservice.org/dev/#/signup</a>'
    )
    api_docs_link.setObjectName("linkLabel")
    api_docs_link.setOpenExternalLinks(True)
    api_docs_link.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    api_layout.addWidget(api_docs_link)

    window.show_key_cb = QCheckBox("Show API key")
    window.show_key_cb.toggled.connect(window._toggle_key_visibility)
    api_layout.addWidget(window.show_key_cb)

    button_row = QHBoxLayout()
    window.save_settings_btn = QPushButton("Save API Key")
    window.save_settings_btn.setObjectName("primaryBtn")
    window.save_settings_btn.setFixedHeight(42)
    window.save_settings_btn.clicked.connect(window._save_settings)

    window.clear_settings_btn = QPushButton("Clear")
    window.clear_settings_btn.setObjectName("ghostBtn")
    window.clear_settings_btn.setFixedHeight(42)
    window.clear_settings_btn.clicked.connect(window._clear_api_key)

    button_row.addWidget(window.save_settings_btn)
    button_row.addWidget(window.clear_settings_btn)

    api_layout.addLayout(button_row)

    window.settings_status = QLabel("")
    window.settings_status.setObjectName("infoBody")
    api_layout.addWidget(window.settings_status)

    info_card = _make_card("heroCard")
    info_layout = QVBoxLayout(info_card)
    info_layout.setContentsMargins(18, 16, 18, 18)
    info_layout.setSpacing(10)

    info_layout.addWidget(_section_title("Project Info"))

    summary_title = QLabel("What this project does")
    summary_title.setObjectName("infoTitle")
    info_layout.addWidget(summary_title)

    summary = QLabel(
        "Trip Calculator estimates route distance, fuel usage, and expected trip cost using real road-distance data from OpenRouteService."
    )
    summary.setObjectName("infoBody")
    summary.setWordWrap(True)
    info_layout.addWidget(summary)

    stack_title = QLabel("Stack")
    stack_title.setObjectName("infoTitle")
    info_layout.addWidget(stack_title)

    stack = QLabel("Python, PySide6, requests, openpyxl")
    stack.setObjectName("infoBody")
    stack.setWordWrap(True)
    info_layout.addWidget(stack)

    contribute_title = QLabel("Contribute")
    contribute_title.setObjectName("infoTitle")
    info_layout.addWidget(contribute_title)

    repo = QLabel('<a href="https://github.com/Ethan-Olowo/tripCalculator">github.com/Ethan-Olowo/tripCalculator</a>')
    repo.setObjectName("linkLabel")
    repo.setOpenExternalLinks(True)
    repo.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
    info_layout.addWidget(repo)

    layout.addWidget(api_card)
    layout.addWidget(info_card)
    layout.addStretch()

    scroll.setWidget(body)
    return scroll
