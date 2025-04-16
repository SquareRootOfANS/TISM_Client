from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QHeaderView, QLineEdit
)
from PyQt6.QtGui import QFont, QColor, QBrush
from PyQt6.QtCore import Qt

class InvestmentPage(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        header_label = QLabel("Investment Share Calculator")
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 12px;")
        layout.addWidget(header_label)

        self.table = QTableWidget(0, 2)
        self.table.setHorizontalHeaderLabels(["Name", "Amount Contributed"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setStyleSheet("font-size: 14px;")
        header_font = QFont()
        header_font.setBold(True)
        self.table.horizontalHeader().setFont(header_font)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.add_row_btn = QPushButton("+ Add Row")
        self.add_row_btn.setStyleSheet("padding: 6px 12px; font-size: 14px; background-color: #444; color: white; border-radius: 4px;")
        self.remove_row_btn = QPushButton("- Remove Selected")
        self.remove_row_btn.setStyleSheet("padding: 6px 12px; font-size: 14px; background-color: #800; color: white; border-radius: 4px;")
        btn_layout.addWidget(self.add_row_btn)
        btn_layout.addWidget(self.remove_row_btn)
        layout.addLayout(btn_layout)

        self.sale_amount_input = QLineEdit()
        self.sale_amount_input.setPlaceholderText("Enter total sale amount")
        self.sale_amount_input.setStyleSheet("padding: 6px; font-size: 14px;")
        layout.addWidget(self.sale_amount_input)

        self.calculate_btn = QPushButton("Calculate Shares")
        self.calculate_btn.setStyleSheet("padding: 6px 12px; font-size: 14px; background-color: #2a5; color: white; border-radius: 4px;")
        layout.addWidget(self.calculate_btn)

        self.results_label = QLabel("")
        self.results_label.setStyleSheet("padding: 8px; font-size: 14px;")
        layout.addWidget(self.results_label)

        self.setLayout(layout)

        self.add_row_btn.clicked.connect(self.add_row)
        self.remove_row_btn.clicked.connect(self.remove_selected_row)
        self.calculate_btn.clicked.connect(self.calculate_shares)

    def add_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)
        for col in range(2):
            item = QTableWidgetItem("")
            if row % 2 == 0:
                item.setBackground(QBrush(QColor("#f8f8f8")))
            self.table.setItem(row, col, item)

    def remove_selected_row(self):
        selected = self.table.currentRow()
        if selected >= 0:
            self.table.removeRow(selected)

    def calculate_shares(self):
        total_sale = self.sale_amount_input.text()
        try:
            total_sale = float(total_sale)
        except ValueError:
            self.results_label.setText("Invalid sale amount.")
            return

        contributors = []
        total_contributed = 0

        for row in range(self.table.rowCount()):
            name_item = self.table.item(row, 0)
            amount_item = self.table.item(row, 1)

            if name_item and amount_item:
                name = name_item.text()
                try:
                    amount = float(amount_item.text())
                    contributors.append((name, amount))
                    total_contributed += amount
                except ValueError:
                    continue

        if total_contributed == 0:
            self.results_label.setText("Total contributions must be greater than 0.")
            return

        results = ""
        for name, amount in contributors:
            percent = (amount / total_contributed * 100)
            share = total_sale * (percent / 100)
            results += f"{name}: {percent:.1f}% share = {share:.2f} aUEC\n"

        self.results_label.setText(results)
