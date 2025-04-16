from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGridLayout, QFrame, QHBoxLayout, QPushButton
)
from PyQt6.QtGui import QPixmap, QPainter
from PyQt6.QtCore import Qt
from services.api_client import fetch_commodity_prices
import requests


class HomePage(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.background = QPixmap("assets/images/home_bg.jpg")  # Load background image
        self.init_ui()

    def init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(20)

        # Title
        title = QLabel("")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        title.setStyleSheet("background-color: transparent;")  # Make transparent
        self.layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16px;
            color: gray;
            margin-bottom: 20px;
            background-color: transparent;  /* Make transparent */
        """)
        self.layout.addWidget(subtitle)

        # === Dynamic data ===
        top_commodity = self.get_top_commodity()
        api_status = self.check_api_status()
        org_update = self.get_org_update()

        # === Cards grid ===
        grid = QGridLayout()
        grid.setSpacing(15)

        def create_card(title, content):
            card = QFrame()
            card.setStyleSheet("""
                background-color: rgba(0, 0, 0, 180);
                padding: 12px;
                border: 1px solid #00ffff;
                border-radius: 10px;
            """)
            card_layout = QVBoxLayout(card)
            title_label = QLabel(title)
            title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #00ffff;")
            content_label = QLabel(content)
            content_label.setStyleSheet("color: white;")
            content_label.setWordWrap(True)
            card_layout.addWidget(title_label)
            card_layout.addWidget(content_label)
            return card

        # API Status
        grid.addWidget(create_card("🔧 API Status", api_status), 0, 0, 1, 1)
        # Org Updates
        grid.addWidget(create_card("📢 Org Updates", org_update), 0, 1, 1, 1)
        # Top Commodity
        grid.addWidget(create_card("📈 Top Commodity", top_commodity), 1, 0, 1, 1)
        # Useful Links
        grid.addWidget(create_card("🔗 Useful Links", "Coming soon..."), 1, 1, 1, 1)

        self.layout.addLayout(grid)

        # === Action Buttons ===
        button_row = QHBoxLayout()
        for label, page in [
            ("Open Trade Tracker", "tracker"),
            ("Open Investments", "investments"),
            ("Plan Route", "route_planner"),
            ("Settings", "settings")
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(0, 255, 255, 80);
                    color: white;
                    border: 1px solid #00ffff;
                    border-radius: 6px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #00ffff;
                    color: black;
                }
            """)
            btn.clicked.connect(lambda _, p=page: self.navigate_callback(p))
            button_row.addWidget(btn)
        self.layout.addLayout(button_row)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self.background.isNull():
            painter.drawPixmap(self.rect(), self.background)

    def get_top_commodity(self):
        try:
            data, _ = fetch_commodity_prices()
            best = None
            max_profit = -float("inf")
            for item in data:
                name = item.get("name")
                buys = [e for e in item["locations"] if e["type"] == "buy"]
                sells = [e for e in item["locations"] if e["type"] == "sell"]
                if not buys or not sells:
                    continue
                best_buy = min(buys, key=lambda x: x["price"])
                best_sell = max(sells, key=lambda x: x["price"])
                profit = best_sell["price"] - best_buy["price"]
                if profit > max_profit:
                    max_profit = profit
                    best = f"{name}\nBuy: {best_buy['location']}\nSell: {best_sell['location']}\nProfit: ~{int(profit):,} aUEC"
            return best or "No data available"
        except Exception as e:
            return f"Error loading data:\n{e}"

    def check_api_status(self):
        status = []
        try:
            r1 = requests.get("https://api.uexcorp.space/2.0/commodities_prices_all", timeout=3)
            status.append("UEX: Online" if r1.ok else "UEX: Offline")
        except:
            status.append("UEX: Offline")
        try:
            r2 = requests.get("https://sc-trade.tools/api/locations", timeout=3)
            status.append("SC Tools: Online" if r2.ok else "SC Tools: Offline")
        except:
            status.append("SC Tools: Offline")
        return "\n".join(status)

    def get_org_update(self):
        return "Lorem ipsum dolor sit amet."
