from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit,
    QTextEdit, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QFormLayout
)
from PyQt6.QtCore import Qt
from services.mission_board import Mission, MissionBoard

class MissionBoardPage(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.board = MissionBoard()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # Title
        title = QLabel("Mission Board")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setObjectName("Title")
        layout.addWidget(title)

        # === Mission Creation Form ===
        form = QFormLayout()
        self.title_input = QLineEdit()
        self.type_input = QComboBox()
        self.type_input.addItems(["Trade Run", "Bounty Hunt", "Recon", "Escort", "Other"])
        self.priority_input = QComboBox()
        self.priority_input.addItems(["Low", "Normal", "High"])
        self.location_input = QLineEdit()
        self.description_input = QTextEdit()

        form.addRow("Title:", self.title_input)
        form.addRow("Type:", self.type_input)
        form.addRow("Priority:", self.priority_input)
        form.addRow("Location:", self.location_input)
        form.addRow("Description:", self.description_input)

        layout.addLayout(form)

        # === Buttons ===
        button_row = QHBoxLayout()
        self.create_button = QPushButton("Create Mission")
        self.clear_button = QPushButton("Clear")
        button_row.addWidget(self.create_button)
        button_row.addWidget(self.clear_button)
        layout.addLayout(button_row)

        # === Mission Table ===
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Title", "Type", "Priority", "Location", "Status", "Action"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Button connections
        self.create_button.clicked.connect(self.handle_create)
        self.clear_button.clicked.connect(self.clear_form)

        self.setLayout(layout)

    def handle_create(self):
        title = self.title_input.text().strip()
        mission_type = self.type_input.currentText()
        priority = self.priority_input.currentText()
        location = self.location_input.text().strip()
        description = self.description_input.toPlainText().strip()

        if not title or not location:
            print("[WARN] Title and Location are required.")
            return

        mission = Mission(title, mission_type, priority, location, description)
        self.board.add_mission(mission)
        self.refresh_table()
        self.clear_form()

    def refresh_table(self):
        self.table.setRowCount(0)
        for idx, mission in enumerate(self.board.get_active_missions()):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(mission.title))
            self.table.setItem(idx, 1, QTableWidgetItem(mission.type))
            self.table.setItem(idx, 2, QTableWidgetItem(mission.priority))
            self.table.setItem(idx, 3, QTableWidgetItem(mission.location))
            self.table.setItem(idx, 4, QTableWidgetItem(mission.status))

            btn = QPushButton("Complete")
            btn.clicked.connect(lambda _, i=idx: self.complete_mission(i))
            self.table.setCellWidget(idx, 5, btn)

    def complete_mission(self, index):
        self.board.mark_completed(index)
        self.refresh_table()

    def clear_form(self):
        self.title_input.clear()
        self.location_input.clear()
        self.description_input.clear()
        self.type_input.setCurrentIndex(0)
        self.priority_input.setCurrentIndex(1)  # Default to Normal

