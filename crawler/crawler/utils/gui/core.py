from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QLabel, QPushButton, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

from functools import partial

import logging
import os.path
import sys

from crawler.version import __version__
from crawler.utils.connection.client import Client

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
        self.__ip__ = '192.168.0.103'
        self.__port__ = 8888
        self.__connection__ = None

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
        self.__lw_send_button__()
        self.__lw_udp_data_entry__()

    def __lw_udp_data_entry__(self):
        """__lw_udp_data_entry__

            Load line edit entry used to send data to Crawler.
        :return:
        """
        self.udp_data_entry = QLineEdit(self)
        self.udp_data_entry.move(20, 95)
        self.udp_data_entry.resize(500, 20)
        self.udp_data_entry.show()

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
        self.connect_button.clicked.connect(self.connect)
        self.connect_button.show()

    def __lw_send_button__(self):
        """__lw_send_button__

            Load button used to send data to Crawler.
        :return: None
        """
        self.send_button = QPushButton('SEND UDP DATA', self)
        self.send_button.resize(self.send_button.sizeHint())
        self.send_button.move(20, 70)
        self.send_button.setToolTip('send to Crawler')
        self.send_button.clicked.connect(self.send_data_and_await_response)
        self.send_button.show()

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

    def connect(self):
        """connect

            Connect to Crawler.
        :return:
        """
        self.__connection__ = Client(host=self.__ip__, port=self.__port__)
        self.__connection__.connect_to_host()

    def send_data_and_await_response(self):
        """
        
        :param data: 
        :return: 
        """
        data = self.udp_data_entry.text()
        response = self.__connection__.send_package_and_get_response(data)
        LOGGER.info(response)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrawlerGUI()

    sys.exit(app.exec_())
