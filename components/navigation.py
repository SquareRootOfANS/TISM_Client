from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

class NavigationBar(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.buttons = {}
        self.active_key = None
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        nav_items = [
            ("homepage", "Home"),
            ("tracker", "Commodity Tracker"),  # 👈 Updated from 'home' to 'tracker'
            ("investments", "Investments"),
            ("route_planner", "Route Planner"),
            ("settings", "Settings")
        ]

        for key, label in nav_items:
            btn = QPushButton(label)
            btn.setProperty("nav_key", key)
            btn.clicked.connect(lambda _, k=key: self.navigate_callback(k))
            self.buttons[key] = btn
            layout.addWidget(btn)

        self.setLayout(layout)

    def set_active_button(self, key):
        self.active_key = key
        for k, btn in self.buttons.items():
            if k == key:
                btn.setStyleSheet("background-color: #005577; color: white; font-weight: bold;")
            else:
                btn.setStyleSheet("")
