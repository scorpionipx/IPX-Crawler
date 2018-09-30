from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QLabel, QPushButton, QInputDialog
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

from functools import partial

import logging
import os.path
import sys

from crawler.version import __version__

LOGGER = logging.getLogger('crawler')
LOGGER.level = logging.INFO

APP_TITLE = 'CrawlerIPX'
APP_SIZE_WIDTH = 800
APP_SIZE_HEIGHT = 600

CURRENT_DIR = os.path.dirname(__file__)


class CrawlerGUI(QWidget):
    """CrawlerGUI

        GUI(Graphical User Interface) app used to control Crawler.
    """

    def __init__(self):
        """Constructor

        """
        self.__ip__ = None
        self.__port__ = None

        super().__init__()

        self.init_gui()

    def init_gui(self):
        """
            Method initializes application's GUI(Graphical User Interface)
        """
        self.__load_window__()
        self.__load_widgets__()

    def centre(self):
        """
        Center the window on screen. This implementation will handle the window
        being resized or the screen resolution changing.
        """
        # Get the current screens' dimensions...
        screen = QDesktopWidget().screenGeometry()
        # ... and get this windows' dimensions
        app_dimensions = self.geometry()
        # The horizontal position is calculated as screenwidth - window's width /2
        h_pos = (screen.width() - app_dimensions.width()) / 2
        # And vertical position the same, but with the height dimensions
        v_pos = (screen.height() - app_dimensions.height()) / 2
        # And the move call repositions the window
        self.move(h_pos, v_pos)

    def __load_widgets__(self):
        """__load_widgets__

            Load application's widgets.
        :return: None
        """
        self.__lw_settings_button__()
        self.__lw_connect_button__()
        # self.__lw_hcu__()
        # self.__lw_ecu__()
        # self.__lw_imess__()

    def __lw_imess__(self):
        """__lw_imess__

            Load widgets used to draw imess connector.
        :return: None
        """
        x_pos = 180
        y_pos = 140
        imess_length = 500
        imess_width = 50
        draw_width = 3
        imess_color = "000000"

        imess_h = QLabel(self)
        imess_h.resize(imess_width, draw_width)
        imess_h.move(x_pos, y_pos)
        imess_h.setStyleSheet("background-color:#" + imess_color)
        imess_h.show()

        imess_h = QLabel(self)
        imess_h.resize(imess_width + draw_width, draw_width)
        imess_h.move(x_pos, y_pos + imess_length)
        imess_h.setStyleSheet("background-color:#" + imess_color)
        imess_h.show()

        imess_v = QLabel(self)
        imess_v.resize(draw_width, imess_length)
        imess_v.move(x_pos, y_pos)
        imess_v.setStyleSheet("background-color:#" + imess_color)
        imess_v.show()

        imess_v = QLabel(self)
        imess_v.resize(draw_width, imess_length)
        imess_v.move(x_pos + imess_width, y_pos)
        imess_v.setStyleSheet("background-color:#" + imess_color)
        imess_v.show()

        text_font = QFont()
        text_font.setPointSize(16)
        text_font.setBold(True)

        imess_name = QLabel(self)
        imess_name.setText('I\nM\nE\nS\nS')
        imess_name.setFont(text_font)
        imess_name.resize(imess_name.sizeHint())
        imess_name.move(192, 300)
        imess_name.show()

    def __lw_hcu__(self):
        """__lw_hcu__

            Load widgets used to draw HCU DB50 connector.
        :return: None
        """
        x_pos = 1170
        y_pos = 100
        hcu_length = 790
        hcu_width = 80
        draw_width = 3
        hcu_color = "000000"

        hcu_h = QLabel(self)
        hcu_h.resize(hcu_width, draw_width)
        hcu_h.move(x_pos, y_pos)
        hcu_h.setStyleSheet("background-color:#" + hcu_color)
        hcu_h.show()

        hcu_h = QLabel(self)
        hcu_h.resize(hcu_width + draw_width, draw_width)
        hcu_h.move(x_pos, y_pos + hcu_length)
        hcu_h.setStyleSheet("background-color:#" + hcu_color)
        hcu_h.show()

        hcu_v = QLabel(self)
        hcu_v.resize(draw_width, hcu_length)
        hcu_v.move(x_pos, y_pos)
        hcu_v.setStyleSheet("background-color:#" + hcu_color)
        hcu_v.show()

        hcu_v = QLabel(self)
        hcu_v.resize(draw_width, hcu_length)
        hcu_v.move(x_pos + hcu_width, y_pos)
        hcu_v.setStyleSheet("background-color:#" + hcu_color)
        hcu_v.show()

        text_font = QFont()
        text_font.setPointSize(16)
        text_font.setBold(True)

        hcu_name = QLabel(self)
        hcu_name.setText('HCU')
        hcu_name.setFont(text_font)
        hcu_name.resize(hcu_name.sizeHint())
        hcu_name.move(1182, 500)
        hcu_name.show()

    def __lw_ecu__(self):
        """__lw_ecu__

            Load widgets used to draw ecu DB50 connector.
        :return: None
        """
        x_pos = 50
        y_pos = 100
        ecu_length = 790
        ecu_width = 80
        draw_width = 3
        ecu_color = "000000"

        ecu_h = QLabel(self)
        ecu_h.resize(ecu_width, draw_width)
        ecu_h.move(x_pos, y_pos)
        ecu_h.setStyleSheet("background-color:#" + ecu_color)
        ecu_h.show()

        ecu_h = QLabel(self)
        ecu_h.resize(ecu_width + draw_width, draw_width)
        ecu_h.move(x_pos, y_pos + ecu_length)
        ecu_h.setStyleSheet("background-color:#" + ecu_color)
        ecu_h.show()

        ecu_v = QLabel(self)
        ecu_v.resize(draw_width, ecu_length)
        ecu_v.move(x_pos, y_pos)
        ecu_v.setStyleSheet("background-color:#" + ecu_color)
        ecu_v.show()

        ecu_v = QLabel(self)
        ecu_v.resize(draw_width, ecu_length)
        ecu_v.move(x_pos + ecu_width, y_pos)
        ecu_v.setStyleSheet("background-color:#" + ecu_color)
        ecu_v.show()

        text_font = QFont()
        text_font.setPointSize(16)
        text_font.setBold(True)

        ecu_name = QLabel(self)
        ecu_name.setText('ECU')
        ecu_name.setAlignment(Qt.AlignCenter)
        ecu_name.setFont(text_font)
        ecu_name.resize(ecu_name.sizeHint())
        ecu_name.move(64, 500)
        ecu_name.show()

    def __lw_settings_button__(self):
        """__lw_settings_button__

            Load button used to configure settings.
        :return: None
        """
        self.settings_button = QPushButton('SETTINGS', self)
        self.settings_button.resize(self.settings_button.sizeHint())
        self.settings_button.move(20, 20)
        self.settings_button.setToolTip('Configure settings')
        self.settings_button.clicked.connect(self.get_settings)
        self.settings_button.show()

    def __lw_connect_button__(self):
        """__lw_connect_button__

            Load button used to connect to Crawler.
        :return: None
        """
        self.connect_button = QPushButton('CONNECT', self)
        self.connect_button.resize(self.connect_button.sizeHint())
        self.connect_button.move(20, 45)
        self.connect_button.setToolTip('Connect to Crawler')
        self.connect_button.show()

    def __load_window__(self):
        """__load_window__

            Method configures main properties of the application's window.
        :return: None
        """
        self.setGeometry(300, 300, APP_SIZE_WIDTH, APP_SIZE_HEIGHT)
        self.setWindowTitle(APP_TITLE)
        self.centre()
        # prevent window from resizing
        self.setFixedSize(self.size())
        self.show()

    def get_settings(self):
        """get_settings

            Pop-up windows dialog to load settings for connection.
        :return: None
        """
        LOGGER.info("Configuring settings")
        ip, ok = QInputDialog.getText(self, 'SETTINGS', 'IP:')
        if ok:
            LOGGER.info("IP: {}".format(ip))
            self.__ip__ = ip
            port, ok = QInputDialog.getInt(self, 'SETTINGS', 'PORT:')
            if ok:
                LOGGER.info("PORT: {}".format(port))
                self.__port__ = port





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrawlerGUI()

    sys.exit(app.exec_())
