import sys
import logging

from PyQt5.QtWidgets import QApplication
from login_components.MainView import LoginWindowView
from old_version.utils import center_window


def begin_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("application.log"),
            logging.StreamHandler()
        ]
    )


def main():
    begin_logging()
    app = QApplication(sys.argv)
    window = LoginWindowView()
    window.show()
    center_window(window)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
