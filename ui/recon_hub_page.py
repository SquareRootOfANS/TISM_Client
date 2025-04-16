# ui/recon_hub_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt
from datetime import datetime
from services.backend_client import submit_recon_report, get_all_recon_reports, delete_recon_report

class ReconHubPage(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.reports = []
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        title = QLabel("Recon Hub")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        layout.addWidget(title)

        form = QFormLayout()
        self.zone_input = QLineEdit()
        self.risk_input = QComboBox()
        self.risk_input.addItems(["Low", "Moderate", "High", "Critical"])
        self.notes_input = QTextEdit()

        form.addRow("Zone:", self.zone_input)
        form.addRow("Risk Level:", self.risk_input)
        form.addRow("Notes:", self.notes_input)
        layout.addLayout(form)

        button_row = QHBoxLayout()
        self.submit_btn = QPushButton("Submit Report")
        self.submit_btn.clicked.connect(self.submit_report)
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected_report)

        button_row.addWidget(self.submit_btn)
        button_row.addWidget(self.delete_btn)
        layout.addLayout(button_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Zone", "Risk Level", "Notes"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.refresh_table()

    def submit_report(self):
        zone = self.zone_input.text().strip()
        risk = self.risk_input.currentText()
        notes = self.notes_input.toPlainText().strip()

        if not zone:
            return

        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "zone": zone,
            "risk": risk,
            "notes": notes
        }

        try:
            submit_recon_report(report)
            self.zone_input.clear()
            self.notes_input.clear()
            self.refresh_table()
        except Exception as e:
            print(f"[ERROR] Failed to submit report: {e}")

    def delete_selected_report(self):
        row = self.table.currentRow()
        if row >= 0 and row < len(self.reports):
            report = self.reports[-(row + 1)]  # Reverse order in table
            report_id = report.get("id")
            if report_id:
                try:
                    delete_recon_report(report_id)
                    self.refresh_table()
                except Exception as e:
                    print(f"[ERROR] Failed to delete report: {e}")

    def refresh_table(self):
        try:
            self.reports = get_all_recon_reports()
        except Exception as e:
            print(f"[ERROR] Failed to load reports: {e}")
            self.reports = []

        self.table.setRowCount(0)
        for report in reversed(self.reports):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(report.get("timestamp", "")))
            self.table.setItem(row, 1, QTableWidgetItem(report.get("zone", "")))
            self.table.setItem(row, 2, QTableWidgetItem(report.get("risk", "")))
            self.table.setItem(row, 3, QTableWidgetItem(report.get("notes", "")))
