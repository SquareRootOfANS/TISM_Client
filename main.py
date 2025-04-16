import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtCore import Qt
from ui.homepage import HomePage
from PyQt6.QtGui import QPixmap
from ui.commodity_tracker import CommodityTrackerPage
from ui.investment_splitter import InvestmentPage
from ui.settings import SettingsPage
from ui.route_planner import RoutePlannerPage
from components.radial_menu import RadialMenu
from services.themes import theme_map
from services.config import app_settings
from ui.loading_screen import LoadingScreen
from ui.MissionBoardPage import MissionBoardPage
from ui.recon_hub_page import ReconHubPage
import os

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TISM Corp Org Tracker")
        self.setGeometry(100, 100, 1200, 800)

        # Define self.pages before assigning any entries to it
        self.pages = {}

        print("[DEBUG] Creating stacked widget")
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.route_planner_prefill = {}

        # Now it's safe to assign loading screen
        self.pages["loading"] = LoadingScreen(navigate_callback=self.navigate_to)
        self.stack.addWidget(self.pages["loading"])
        self.stack.setCurrentWidget(self.pages["loading"])

        print("[DEBUG] Initializing pages")
        self.pages["homepage"] = HomePage(navigate_callback=self.navigate_to)
        self.pages["tracker"] = CommodityTrackerPage(
            navigate_callback=self.navigate_to,
            set_route_prefill_callback=self.set_route_planner_prefill
        )
        self.pages["investments"] = InvestmentPage(navigate_callback=self.navigate_to)
        self.pages["loading"] = LoadingScreen(navigate_callback=self.navigate_to)
        self.pages["homepage"] = HomePage(navigate_callback=self.navigate_to)
        self.pages["mission_board"] = MissionBoardPage(navigate_callback=self.navigate_to)
        self.pages["settings"] = SettingsPage(navigate_callback=self.navigate_to)
        self.pages["recon_hub"] = ReconHubPage(navigate_callback=self.navigate_to)
        
        
        self.pages["route_planner"] = RoutePlannerPage(
            navigate_callback=self.navigate_to,
            get_prefill_callback=lambda: self.route_planner_prefill
        )

        for page in self.pages.values():
            self.stack.addWidget(page)

        self.stack.setCurrentWidget(self.pages["loading"])
        print("[DEBUG] MainApp setup complete")

    def navigate_to(self, page_name):
        widget = self.pages.get(page_name)
        if widget:
            index = self.stack.indexOf(widget)
            print(f"[DEBUG] Switching to page '{page_name}' at index {index}")
            self.stack.setCurrentIndex(index)

            if page_name == "route_planner":
                self.pages["route_planner"].set_prefilled_fields()

    def set_route_planner_prefill(self, data):
        self.route_planner_prefill = data

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if RadialMenu.active_menu:
                RadialMenu.active_menu.close()
            else:
                menu = RadialMenu(self, navigate_callback=self.navigate_to)
                menu.move(
                    self.width() // 2 - menu.width() // 2,
                    self.height() // 2 - menu.height() // 2
                )
                menu.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    selected_theme = app_settings.get("theme", "Default").strip()
    stylesheet = theme_map.get(selected_theme)

    if stylesheet:
        app.setStyleSheet(stylesheet)
        print(f"[DEBUG] Applied theme: {selected_theme}")
    else:
        print(f"[WARN] Theme '{selected_theme}' not found. Using no stylesheet.")

    main_window = MainApp()
    main_window.showFullScreen()
    sys.exit(app.exec())