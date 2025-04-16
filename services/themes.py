# themes.py

Dark_qss = """
QWidget {
    background-color: #0a0a0a;
    color: #e0f7ff;
    font-family: "Orbitron", "Segoe UI", "Roboto", sans-serif;
    font-size: 14px;
}
QLabel#Title {
    font-size: 28px;
    font-weight: 600;
    color: #00ffe7;
    padding: 10px;
    text-shadow: 0 0 5px #00ffe7;
}
QPushButton {
    background-color: #111;
    color: #00ffff;
    border: 1px solid #00bfbf;
    padding: 8px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #00bfbf;
    color: #000;
    font-weight: bold;
}
QLineEdit, QComboBox, QPlainTextEdit, QTextEdit {
    background-color: #141414;
    color: #cfffff;
    border: 1px solid #007777;
    border-radius: 4px;
    padding: 4px;
}
QTableWidget {
    background-color: #101010;
    color: #aeefff;
    gridline-color: #222;
    border: 1px solid #007777;
}
QHeaderView::section {
    background-color: #003333;
    color: #00ffff;
    font-weight: bold;
    padding: 4px;
    border: 1px solid #006666;
}
QScrollBar:vertical {
    background: #111;
    width: 10px;
}
QScrollBar::handle:vertical {
    background: #00d9ff;
    border-radius: 5px;
}
QPushButton[active="true"] {
    background-color: #007777;
    color: #fff;
    font-weight: bold;
    border: 1px solid #00ffee;
}
QPushButton#ExitButton {
    background-color: #111;
    color: #00ffff;
    border: 2px solid #00ffff;
    border-radius: 16px;
    padding: 6px;
    min-width: 32px;
    min-height: 32px;
}
QPushButton#ExitButton:hover {
    background-color: #00ffff;
    color: #000;
}
QPushButton#CloseButton {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border: 2px solid #ff8888;
    border-radius: 30px;
}
QPushButton#CloseButton:hover {
    background-color: white;
    color: #ff0033;
}
QWidget#HomePage {
    background-image: url("assets/images/home_bg.jpg");
    background-repeat: no-repeat;
    background-position: center;
}
QWidget#LoadingScreen {
    background-image: url(assets/images/loading_background.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    background-color: #000; /* fallback in case image fails */
}



"""

microtech_qss = """
QWidget {
    background-color: #101820;
    color: #cceeff;
    font-family: "Roboto", sans-serif;
    font-size: 14px;
}
QLabel#Title {
    color: #72e6ff;
    font-size: 28px;
    font-weight: bold;
    padding: 10px;
}
QPushButton {
    background-color: #142434;
    color: #72e6ff;
    border: 1px solid #3498db;
    padding: 8px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #3498db;
    color: #000;
}
QLineEdit, QComboBox, QTextEdit {
    background-color: #1c2c3c;
    color: #d4f0ff;
    border: 1px solid #3399ff;
    border-radius: 4px;
}
QTableWidget {
    background-color: #1a1f2f;
    color: #e0f4ff;
    gridline-color: #244;
}
QHeaderView::section {
    background-color: #16232f;
    color: #72e6ff;
    border: 1px solid #244;
}
QPushButton#ExitButton {
    background-color: #142434;
    color: #72e6ff;
    border: 2px solid #72e6ff;
    border-radius: 16px;
    padding: 6px;
    min-width: 32px;
    min-height: 32px;
}
QPushButton#ExitButton:hover {
    background-color: #72e6ff;
    color: #000;
}
QPushButton#CloseButton {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border: 2px solid #ff8888;
    border-radius: 30px;
}
QPushButton#CloseButton:hover {
    background-color: white;
    color: #ff0033;
}
QWidget#HomePage {
    background-image: url("assets/images/home_bg.jpg");
    background-repeat: no-repeat;
    background-position: center;
}
QWidget#LoadingScreen {
    background-image: url(assets/images/loading_background.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    background-color: #000; /* fallback in case image fails */
}


"""

hurston_qss = """
QWidget {
    background-color: #1c1a18;
    color: #f0e6d2;
    font-family: "Segoe UI", sans-serif;
    font-size: 14px;
}
QLabel#Title {
    color: #d7b97f;
    font-size: 28px;
    font-weight: bold;
    padding: 10px;
}
QPushButton {
    background-color: #3c2f2f;
    color: #f0e6d2;
    border: 1px solid #b88c3a;
    padding: 8px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #b88c3a;
    color: #000;
}
QLineEdit, QComboBox, QTextEdit {
    background-color: #292522;
    color: #f0e6d2;
    border: 1px solid #b88c3a;
    border-radius: 4px;
}
QTableWidget {
    background-color: #2a2724;
    color: #f5f0e6;
    gridline-color: #4a3f3a;
}
QHeaderView::section {
    background-color: #3c302b;
    color: #d7b97f;
    border: 1px solid #5a4a3a;
}
QPushButton#ExitButton {
    background-color: #3c2f2f;
    color: #d7b97f;
    border: 2px solid #d7b97f;
    border-radius: 16px;
    padding: 6px;
    min-width: 32px;
    min-height: 32px;
}
QPushButton#ExitButton:hover {
    background-color: #d7b97f;
    color: #000;
}
QPushButton#CloseButton {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border: 2px solid #ff8888;
    border-radius: 30px;
}
QPushButton#CloseButton:hover {
    background-color: white;
    color: #ff0033;
}
QWidget#HomePage {
    background-image: url("assets/images/home_bg.jpg");
    background-repeat: no-repeat;
    background-position: center;
}
QWidget#LoadingScreen {
    background-image: url(assets/images/loading_background.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    background-color: #000; /* fallback in case image fails */
}



"""

crusader_qss = """
QWidget {
    background-color: #1c1b21;
    color: #ffffff;
    font-family: "Segoe UI", sans-serif;
    font-size: 14px;
}
QLabel#Title {
    color: #ff4455;
    font-size: 28px;
    font-weight: bold;
    padding: 10px;
}
QPushButton {
    background-color: #2a2a2a;
    color: #ff4455;
    border: 1px solid #ff7788;
    padding: 8px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #ff4455;
    color: #fff;
}
QLineEdit, QComboBox, QTextEdit {
    background-color: #2e2c33;
    color: #ffffff;
    border: 1px solid #ff4455;
    border-radius: 4px;
}
QTableWidget {
    background-color: #242229;
    color: #fff0f0;
    gridline-color: #444;
}
QHeaderView::section {
    background-color: #3a3339;
    color: #ff4455;
    border: 1px solid #aa5555;
}
QPushButton#ExitButton {
    background-color: #2a2a2a;
    color: #ff4455;
    border: 2px solid #ff4455;
    border-radius: 16px;
    padding: 6px;
    min-width: 32px;
    min-height: 32px;
}
QPushButton#ExitButton:hover {
    background-color: #ff4455;
    color: #fff;
}
QPushButton#CloseButton {
    background-color: #ff0033;
    color: white;
    font-weight: bold;
    border: 2px solid #ff8888;
    border-radius: 30px;
}
QPushButton#CloseButton:hover {
    background-color: white;
    color: #ff0033;
}
QWidget#HomePage {
    background-image: url("assets/images/home_bg.jpg");
    background-repeat: no-repeat;
    background-position: center;
QWidget#LoadingScreen {
    background-image: url(assets/images/loading_background.jpg);
    background-repeat: no-repeat;
    background-position: center;
    background-origin: content;
    background-color: #000; /* fallback in case image fails */
}


"""

theme_map = {
    "Default": Dark_qss,
    "MicroTech": microtech_qss,
    "Hurston": hurston_qss,
    "Crusader": crusader_qss
}
