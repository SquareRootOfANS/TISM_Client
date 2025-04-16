from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QComboBox, QFormLayout, QTextEdit, QCompleter, QLineEdit
)
from PyQt6.QtCore import Qt
from services.api_client import fetch_all_locations


class RoutePlannerPage(QWidget):
    def __init__(self, parent=None, navigate_callback=None, get_prefill_callback=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.get_prefill_callback = get_prefill_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        title = QLabel("Trade Route Planner")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(title)

        form_layout = QFormLayout()

        # === Get all locations ===
        self.all_locations = fetch_all_locations()

        # === Start location search field ===
        self.start_location_input = QLineEdit()
        self.start_location_input.setPlaceholderText("Search for start location...")
        start_completer = QCompleter(self.all_locations)
        start_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        start_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        start_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.start_location_input.setCompleter(start_completer)

        # === Destination location search field ===
        self.dest_location_input = QLineEdit()
        self.dest_location_input.setPlaceholderText("Search for destination...")
        dest_completer = QCompleter(self.all_locations)
        dest_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        dest_completer.setFilterMode(Qt.MatchFlag.MatchContains)
        dest_completer.setCompletionMode(QCompleter.CompletionMode.PopupCompletion)
        self.dest_location_input.setCompleter(dest_completer)

        # === Commodity dropdown ===
        self.commodity_dropdown = QComboBox()
        self.commodity_dropdown.addItems(["Medical Supplies", "Laranite", "Agricium", "Titanium", "Distilled Spirits"])

        # === Add to layout ===
        form_layout.addRow("Start Location:", self.start_location_input)
        form_layout.addRow("Destination Location:", self.dest_location_input)
        form_layout.addRow("Commodity:", self.commodity_dropdown)
        layout.addLayout(form_layout)

        self.plan_button = QPushButton("Plan Route")
        self.plan_button.clicked.connect(self.plan_route)
        layout.addWidget(self.plan_button)

        self.results_box = QTextEdit()
        self.results_box.setReadOnly(True)
        layout.addWidget(self.results_box)

        self.setLayout(layout)

    def plan_route(self):
        start = self.start_location_input.text()
        dest = self.dest_location_input.text()
        commodity = self.commodity_dropdown.currentText()

        self.results_box.setText(
            f"Route from **{start}** to **{dest}** for **{commodity}**:\n\n"
            f"Estimated Fuel Cost: ~350 aUEC\n"
            f"Estimated Travel Time: ~7 min\n"
            f"Potential Profit: ~12,500 aUEC"
        )

    def set_prefilled_fields(self):
        if not self.get_prefill_callback:
            print("[DEBUG] No prefill callback provided.")
            return

        prefill = self.get_prefill_callback()
        print("[DEBUG] Route Planner prefill:", prefill)

        start = prefill.get("location")
        commodity = prefill.get("commodity")

        if start:
            self.start_location_input.setText(start)

        if commodity and commodity in [self.commodity_dropdown.itemText(i) for i in range(self.commodity_dropdown.count())]:
            index = self.commodity_dropdown.findText(commodity, Qt.MatchFlag.MatchFixedString)
            if index != -1:
                self.commodity_dropdown.setCurrentIndex(index)
