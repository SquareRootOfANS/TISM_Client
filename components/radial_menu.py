from PyQt6.QtWidgets import QWidget, QApplication, QGraphicsDropShadowEffect
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QMouseEvent, QPaintEvent
from PyQt6.QtCore import Qt, QPointF, QRectF, QPropertyAnimation, QEasingCurve
import math


class RadialMenu(QWidget):
    active_menu = None  # Class-level tracker

    def __init__(self, parent=None, navigate_callback=None):
        super().__init__(parent)
        self.navigate_callback = navigate_callback
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(300, 300)

        self.center_point = QPointF(self.width() / 2, self.height() / 2)
        self.r_inner = 40
        self.r_outer = 150
        self.hovering_center = False  # Track hover state

        self.current_view = "main"
        self.init_main_quadrants()

        self.move(
            parent.geometry().center().x() - self.width() // 2,
            parent.geometry().center().y() - self.height() // 2
        )

        # Neon glow
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(60)
        glow.setOffset(0)
        glow.setColor(QColor(0, 255, 255, 180))
        self.setGraphicsEffect(glow)

        # Fade in
        self.setWindowOpacity(0)
        self.fade_anim = QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(300)
        self.fade_anim.setStartValue(0)
        self.fade_anim.setEndValue(1)
        self.fade_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.fade_anim.start()

        RadialMenu.active_menu = self

    def init_main_quadrants(self):
        self.quadrants = [
            {"label": "Logistics", "start": -36, "end": 36, "action": self.show_logistics_menu},
            {"label": "Home", "start": 36, "end": 108, "page": "homepage"},
            {"label": "Settings", "start": 108, "end": 180, "page": "settings"},
            {"label": "Admin", "start": 180, "end": 252, "action": self.show_admin_menu},
            {"label": "Exit", "start": 252, "end": 324, "action": self.close_app}
        ]

        self.current_view = "main"
        self.update()

    def show_logistics_menu(self):
        self.current_view = "logistics"
        self.quadrants = [
            {"label": "Tracker", "start": 45, "end": 135, "page": "tracker"},
            {"label": "Investments", "start": 135, "end": 225, "page": "investments"},
            {"label": "Route Plan", "start": 225, "end": 315, "page": "route_planner"},
            {"label": "Back", "start": 315, "end": 405, "action": self.init_main_quadrants}
        ]
        self.update()

    def close_app(self):
        QApplication.instance().quit()

    # filepath: c:\Users\tyler\Documents\VSCode\Projects\SCStocks\components\radial_menu.py
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        outer_rect = QRectF(
            self.center_point.x() - self.r_outer,
            self.center_point.y() - self.r_outer,
            2 * self.r_outer, 2 * self.r_outer
        )

        # Draw the quadrants first
        for quadrant in self.quadrants:
            start_angle = quadrant["start"]
            span_angle = quadrant["end"] - quadrant["start"]

            painter.setBrush(QBrush(QColor(20, 60, 80, 160)))
            painter.setPen(QPen(QColor(0, 255, 255, 150), 2))
            painter.drawPie(outer_rect, -start_angle * 16, -span_angle * 16)

            mid_angle = math.radians((quadrant["start"] + quadrant["end"]) / 2)
            label_x = self.center_point.x() + (self.r_inner + self.r_outer) / 2 * math.cos(mid_angle)
            label_y = self.center_point.y() - (self.r_inner + self.r_outer) / 2 * math.sin(mid_angle)

            painter.setPen(QColor(0, 255, 255))
            painter.drawText(int(label_x - 30), int(label_y + 5), quadrant["label"])

        # Mask the center area to hide quadrant borders
        painter.setBrush(QColor(20, 60, 80, 255))  # Fully opaque to mask
        painter.setPen(Qt.PenStyle.NoPen)  # No border for the mask
        painter.drawEllipse(self.center_point, self.r_inner + 2, self.r_inner + 2)

        # Draw the center button with a matching border
        painter.setBrush(QColor(20, 60, 80, 200))  # Center button fill color
        painter.setPen(QPen(QColor(0, 255, 255, 150), 2))  # Matching border color
        painter.drawEllipse(self.center_point, self.r_inner, self.r_inner)

        if self.hovering_center:
            painter.setPen(QPen(QColor(0, 255, 255, 255), 2, Qt.PenStyle.DashLine))
            painter.drawEllipse(self.center_point, self.r_inner + 3, self.r_inner + 3)

    def mousePressEvent(self, event: QMouseEvent):
        click_pos = event.position()
        dx = click_pos.x() - self.center_point.x()
        dy = self.center_point.y() - click_pos.y()
        dist = math.hypot(dx, dy)

        if dist <= self.r_inner:
            # Return to main or close menu
            if self.current_view == "main":
                self.close()
            else:
                self.init_main_quadrants()
            return

        if dist > self.r_outer:
            return

        angle = math.degrees(math.atan2(dy, dx)) % 360

        for quadrant in self.quadrants:
            start = quadrant["start"] % 360
            end = quadrant["end"] % 360
            if start < end:
                if start <= angle <= end:
                    self.handle_quadrant(quadrant)
                    return
            else:
                if angle >= start or angle <= end:
                    self.handle_quadrant(quadrant)
                    return

    def handle_quadrant(self, quadrant):
        print(f"[DEBUG] Clicked on: {quadrant['label']}")
        if "action" in quadrant:
            quadrant["action"]()
        elif self.navigate_callback and "page" in quadrant:
            self.navigate_callback(quadrant["page"])
            self.close()

    def closeEvent(self, event):
        RadialMenu.active_menu = None
        super().closeEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        dx = event.position().x() - self.center_point.x()
        dy = event.position().y() - self.center_point.y()
        dist = math.hypot(dx, dy)
        hovering = dist <= self.r_inner
        if hovering != self.hovering_center:
            self.hovering_center = hovering
            self.update()
    def show_admin_menu(self):
        self.current_view = "admin"
        self.quadrants = [
            {"label": "Mission Board", "start": 45, "end": 135, "page": "mission_board"},
            {"label": "TBC", "start": 135, "end": 225},
            {"label": "Recon Hub", "start": 225, "end": 315, "page": "recon_hub"},
            {"label": "Back", "start": 315, "end": 405, "action": self.init_main_quadrants}
        ]
        self.update()
