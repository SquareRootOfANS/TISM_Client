from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QMovie, QFont, QColor, QBrush
from PyQt6.QtCore import Qt
from services.api_client import fetch_commodity_prices
from collections import defaultdict

class CommodityTrackerPage(QWidget):
    def __init__(self, parent=None, navigate_callback=None, set_route_prefill_callback=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.set_route_prefill = set_route_prefill_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        header_label = QLabel("Live Commodity Prices", self)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 26px; font-weight: bold; padding: 12px;")
        layout.addWidget(header_label)

        self.warning_banner = QLabel()
        self.warning_banner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.warning_banner.setStyleSheet("color: white; background-color: darkred; padding: 10px; font-weight: bold;")
        self.warning_banner.setVisible(False)
        layout.addWidget(self.warning_banner)

        self.movie_label = QLabel(self)
        self.movie = QMovie("assets/animations/space.gif")
        self.movie_label.setMovie(self.movie)
        self.movie.start()
        self.movie_label.setFixedHeight(100)
        self.movie_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.movie_label)

        search_refresh_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search commodities...")
        self.search_input.setStyleSheet("padding: 6px; font-size: 14px;")
        self.search_input.textChanged.connect(self.filter_table)
        search_refresh_layout.addWidget(self.search_input)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setStyleSheet("padding: 6px 12px; font-size: 14px; background-color: #444; color: white; border-radius: 4px;")
        self.refresh_button.clicked.connect(self.load_commodity_data)
        search_refresh_layout.addWidget(self.refresh_button)
        layout.addLayout(search_refresh_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Commodity", "Best Buy Location", "Buy Price", "Best Sell Location", "Sell Price", "Profit Margin"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setStyleSheet("font-size: 14px;")
        header_font = QFont()
        header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)
        layout.addWidget(self.table)

        self.plan_route_button = QPushButton("Plan Route")
        self.plan_route_button.clicked.connect(self.go_to_route_planner_with_selected)
        layout.addWidget(self.plan_route_button)

        self.setLayout(layout)
        self.load_commodity_data()

    def load_commodity_data(self):
        print("[DEBUG] Fetching enriched data...")
        data, fallback_timestamp = fetch_commodity_prices()
        print("[DEBUG] Got data:", data[:1])
        print("[DEBUG] Fallback:", fallback_timestamp)

        self.table.setRowCount(0)
        self.all_commodities = []

        if fallback_timestamp:
            self.warning_banner.setVisible(True)
            self.warning_banner.setText(f"⚠️ Using cached data from {fallback_timestamp}. Live API may be unavailable.")
        else:
            self.warning_banner.setVisible(False)

        grouped = defaultdict(list)
        for item in data:
            name = item.get("name")
            for loc in item.get("locations", []):
                enriched = {
                    "name": name,
                    "location": loc.get("location"),
                    "path": loc.get("path", "-"),
                    "type": loc.get("type"),
                    "price": loc.get("price"),
                    "is_buy": loc.get("type") == "buy",
                    "is_sell": loc.get("type") == "sell"
                }
                grouped[name].append(enriched)

        print(f"[DEBUG] Grouped {len(grouped)} commodities.")

        for index, (name, entries) in enumerate(grouped.items()):
            buys = [e for e in entries if e["is_buy"] and e["price"]]
            sells = [e for e in entries if e["is_sell"] and e["price"]]

            best_buy = min(buys, key=lambda x: x["price"], default=None)
            best_sell = max(sells, key=lambda x: x["price"], default=None)

            self.all_commodities.append({
                "name": name,
                "bestBuy": best_buy,
                "bestSell": best_sell
            })

            self.add_table_row(name, best_buy, best_sell, index)

    def add_table_row(self, name, best_buy, best_sell, index):
        buy_loc = best_buy.get("path") if best_buy else "-"
        sell_loc = best_sell.get("path") if best_sell else "-"
        buy_price = best_buy.get("price") if best_buy else None
        sell_price = best_sell.get("price") if best_sell else None

        try:
            margin = float(sell_price) - float(buy_price)
            margin_str = f"{margin:.2f}"
        except:
            margin_str = "-"

        row_index = self.table.rowCount()
        self.table.insertRow(row_index)

        items = [
            QTableWidgetItem(name),
            QTableWidgetItem(buy_loc),
            QTableWidgetItem(str(buy_price) if buy_price else "-"),
            QTableWidgetItem(sell_loc),
            QTableWidgetItem(str(sell_price) if sell_price else "-"),
            QTableWidgetItem(margin_str)
        ]

        if index % 2 == 0:
            for cell in items:
                cell.setBackground(QBrush(QColor("#1a1a1a")))

        for col, cell in enumerate(items):
            self.table.setItem(row_index, col, cell)

    def go_to_route_planner_with_selected(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            print("[DEBUG] No row selected.")
            return

        row = selected_items[0].row()
        commodity = self.table.item(row, 0).text() if self.table.item(row, 0) else ""
        location = self.table.item(row, 1).text() if self.table.item(row, 1) else ""

        if self.set_route_prefill:
            self.set_route_prefill({
                "commodity": commodity,
                "location": location
            })

        if self.navigate_callback:
            self.navigate_callback("route_planner")

    def filter_table(self):
        search_term = self.search_input.text().lower()
        self.table.setRowCount(0)

        for index, item in enumerate(self.all_commodities):
            name = item.get("name", "").lower()
            if search_term in name:
                self.add_table_row(item["name"], item["bestBuy"], item["bestSell"], index)
