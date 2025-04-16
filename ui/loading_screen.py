from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve

class LoadingScreen(QWidget):
    def __init__(self, navigate_callback=None):
        super().__init__()
        self.navigate_callback = navigate_callback
        self.background = QPixmap("assets/images/loading_background.jpg")  # Load background image
        self.init_ui()

    def init_ui(self):
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # === Background ===
        self.background = QLabel(self)
        self.bg_pixmap = QPixmap("assets/images/loading_background.jpg")
        self.background.setScaledContents(True)
        self.background.lower()

        # === Overlay ===
        self.overlay = QWidget(self)
        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay_layout.setContentsMargins(50, 50, 50, 50)

        # === Title ===
        title = QLabel("Trade, Industry, Security and Management Corp")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
        title.setGraphicsEffect(self._create_glow())
        self.overlay_layout.addWidget(title)

        # === Subtitle ===
        subtitle = QLabel("A.T.L.A.S\nAdvanced Trade Logistics Administrative Solution")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: cyan; font-size: 20px;")
        self.overlay_layout.addWidget(subtitle)

        # === Timed Fade Out ===
        QTimer.singleShot(4000, self.fade_out)

    def _create_glow(self):
        effect = QGraphicsOpacityEffect()
        effect.setOpacity(1.0)
        return effect

    def fade_out(self):
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(2000)
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.finished.connect(lambda: self.navigate_callback("homepage"))
        anim.start()
        self.fade_anim = anim  # prevent garbage collection

    def resizeEvent(self, event):
        if not self.bg_pixmap.isNull():
            scaled = self.bg_pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            self.background.setPixmap(scaled)
            self.background.setGeometry(self.rect())
            self.overlay.setGeometry(self.rect())
        super().resizeEvent(event)
