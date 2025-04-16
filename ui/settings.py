from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox, QFormLayout, QApplication
)
from PyQt6.QtCore import Qt
from components.navigation import NavigationBar
from services.themes import theme_map
from services.config import app_settings


class SettingsPage(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        nav = NavigationBar(navigate_callback=self.navigate_callback)
        layout.addWidget(nav)
        nav.set_active_button("settings")

        title = QLabel("Settings")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        layout.addWidget(title)

        form = QFormLayout()

        # 🌌 Theme selector
        self.theme_dropdown = QComboBox()
        self.theme_dropdown.addItems(theme_map.keys())

        current_theme = app_settings.get("theme", "Default")
        if current_theme not in theme_map:
            print(f"[WARN] Stored theme '{current_theme}' not found in theme_map.")
            current_theme = list(theme_map.keys())[0]

        self.theme_dropdown.setCurrentText(current_theme)
        self.theme_dropdown.currentTextChanged.connect(self.apply_theme)
        form.addRow("Theme:", self.theme_dropdown)

        # 🔁 Auto refresh interval
        self.refresh_rate = QComboBox()
        self.refresh_rate.addItems(["Disabled", "1 min", "5 min", "15 min"])
        self.refresh_rate.setCurrentText(app_settings.get("refresh_rate", "Disabled"))
        self.refresh_rate.currentTextChanged.connect(self.set_refresh_rate)
        form.addRow("Auto Refresh:", self.refresh_rate)

        # 🌐 API source selection
        self.api_selector = QComboBox()
        self.api_selector.addItems(["SC Trade Tools", "UEX"])
        self.api_selector.setCurrentText(app_settings.get("api_source", "SC Trade Tools"))
        self.api_selector.currentTextChanged.connect(self.set_api_source)
        form.addRow("API Source:", self.api_selector)

        # 👥 Remember contributors toggle
        self.save_contributors_checkbox = QCheckBox("Remember last contributor list")
        self.save_contributors_checkbox.setChecked(app_settings.get("remember_contributors", False))
        self.save_contributors_checkbox.stateChanged.connect(self.set_contributor_memory)
        form.addRow("Defaults:", self.save_contributors_checkbox)

        layout.addLayout(form)
        self.setLayout(layout)

    def apply_theme(self, theme_name):
        theme = theme_map.get(theme_name)
        if theme:
            QApplication.instance().setStyleSheet(theme)
            app_settings["theme"] = theme_name
            print(f"[DEBUG] Theme changed to: {theme_name}")
        else:
            print(f"[WARN] Theme '{theme_name}' not found. Using no stylesheet.")

    def set_api_source(self, value):
        app_settings["api_source"] = value
        print(f"[DEBUG] API source set to: {value}")

    def set_refresh_rate(self, value):
        app_settings["refresh_rate"] = value
        print(f"[DEBUG] Refresh rate set to: {value}")

    def set_contributor_memory(self, state):
        app_settings["remember_contributors"] = bool(state)
        print(f"[DEBUG] Remember contributors: {bool(state)}")
