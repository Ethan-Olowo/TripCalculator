from PySide6.QtWidgets import QFrame, QHBoxLayout, QScrollArea, QVBoxLayout, QWidget


def build_planner_page(window):
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QFrame.Shape.NoFrame)

    body = QWidget()
    body.setObjectName("mainPageBody")
    layout = QVBoxLayout(body)
    layout.setContentsMargins(24, 20, 24, 28)
    layout.setSpacing(14)

    activity_card = window._make_activity_card()
    layout.addWidget(activity_card)

    two_col = QHBoxLayout()
    two_col.setSpacing(14)

    left_col = QVBoxLayout()
    left_col.setSpacing(14)
    left_col.addWidget(window._make_route_card())
    left_col.addWidget(window._make_fuel_card())
    left_col.addWidget(window._make_options_card())
    left_col.addWidget(window._make_calculate_button())
    left_col.addStretch()

    right_col = QVBoxLayout()
    right_col.setSpacing(14)
    right_col.addWidget(window._make_results_card())
    right_col.addStretch()

    left_wrap = QWidget()
    left_wrap.setLayout(left_col)
    right_wrap = QWidget()
    right_wrap.setLayout(right_col)

    two_col.addWidget(left_wrap, 3)
    two_col.addWidget(right_wrap, 2)
    layout.addLayout(two_col)
    layout.addStretch()

    scroll.setWidget(body)
    return scroll
