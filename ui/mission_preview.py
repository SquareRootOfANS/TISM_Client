from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFrame
from PyQt6.QtCore import Qt


class MissionPreviewWidget(QWidget):
    def __init__(self, missions, on_view_all=None):
        super().__init__()
        self.missions = missions or []
        self.on_view_all = on_view_all
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(6)

        # Header with title and button
        header_layout = QHBoxLayout()
        title_label = QLabel("🛰️ Active Missions")
        title_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #00ffff;")
        header_layout.addWidget(title_label)

        view_all_btn = QPushButton("View All")
        view_all_btn.setFixedHeight(24)
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #00ffff;
                border: none;
                text-decoration: underline;
                font-size: 13px;
            }
            QPushButton:hover {
                color: #00ccff;
            }
        """)
        view_all_btn.clicked.connect(self.on_view_all)
        header_layout.addStretch()
        header_layout.addWidget(view_all_btn)
        layout.addLayout(header_layout)

        # List up to 3 active missions
        if self.missions:
            for mission in self.missions[:3]:
                line = QLabel(f"• {mission['title']} [{mission['type']}] at {mission['location']}")
                line.setStyleSheet("color: white; font-size: 13px;")
                layout.addWidget(line)
        else:
            no_missions = QLabel("No active missions.")
            no_missions.setStyleSheet("color: gray; font-size: 13px;")
            layout.addWidget(no_missions)

    def set_missions(self, missions):
        """This function can be used to update the displayed missions"""
        self.missions = missions
        self.init_ui()


# Simulated mission list for now
MISSIONS = [
    {"title": "Trade Run to Port Olisar", "type": "Trade", "location": "Stanton"},
    {"title": "Escort Convoy to Area18", "type": "Escort", "location": "Hurston"}
]

def create_active_missions_preview(navigate_callback=None):
    frame = QFrame()
    frame.setStyleSheet("""
        background-color: rgba(0, 0, 0, 180);
        padding: 12px;
        border: 1px solid #00ffff;
        border-radius: 10px;
    """)

    layout = QVBoxLayout(frame)
    title = QLabel("🛰 Active Missions")
    title.setStyleSheet("font-weight: bold; font-size: 16px; color: #00ffff;")
    layout.addWidget(title)

    # Dummy data for preview
    missions = [
        {"title": "Trade Run to Port Olisar"},
        {"title": "Escort to Orison"},
        {"title": "Recon at Grim HEX"},
    ]

    for mission in missions[:3]:
        lbl = QLabel(f"• {mission['title']}")
        lbl.setStyleSheet("color: white;")
        layout.addWidget(lbl)

    # Clicking the widget takes you to the mission board
    if navigate_callback:
        frame.mousePressEvent = lambda e: navigate_callback("mission_board")

    return frame
