from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QLabel, QPushButton, QInputDialog, QLineEdit
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import Qt, QSize

from functools import partial

import logging
import os.path
import sys

from time import sleep

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
        self.__ip__ = '192.168.0.109'
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
        self.__lw_send_udp_button__()
        self.__lw_udp_data_entry__()
        self.__lw_send_spi_button__()
        self.__lw_spi_data_entry__()
        self.__lw_power_data_entry__()
        self.__lw_direction_data_entry__()
        self.__lw_motor_control__()
        self.__lw_lights_control__()
        
    def __lw_motor_control__(self):
        """__lw_motor_control__
        
        :return: 
        """
        x = 380
        y = 260
        
        self.send_power_button = QPushButton('SEND POWER', self)
        self.send_power_button.resize(self.send_power_button.sizeHint())
        self.send_power_button.move(x, y)
        self.send_power_button.setToolTip('Set specified power')
        self.send_power_button.clicked.connect(self.set_power)
        self.send_power_button.show()
        
        self.send_direction_button = QPushButton('SEND DIRECTIONS', self)
        self.send_direction_button.resize(self.send_direction_button.sizeHint())
        self.send_direction_button.move(x, y + 25)
        self.send_direction_button.setToolTip('Set specified direction')
        self.send_direction_button.clicked.connect(self.set_directions)
        self.send_direction_button.show()
        
        self.send_motor_control_data = QPushButton('MOTOR CONTROL', self)
        self.send_motor_control_data.resize(self.send_motor_control_data.sizeHint())
        self.send_motor_control_data.move(x, y + 50)
        self.send_motor_control_data.setToolTip('Set specified power and directions')
        self.send_motor_control_data.clicked.connect(self.set_motor_control)
        self.send_motor_control_data.show()

    def __lw_lights_control__(self):
        """__lw_lights_control__

        :return: 
        """
        x = 500
        y = 260

        self.turn_on_headlights = QPushButton('HEADLIGHTS ON', self)
        self.turn_on_headlights.resize(self.turn_on_headlights.sizeHint())
        self.turn_on_headlights.move(x, y)
        self.turn_on_headlights.setToolTip('Turn on headlights')
        self.turn_on_headlights.clicked.connect(self.turn_lights_on)
        self.turn_on_headlights.show()

        self.turn_off_headlights = QPushButton('HEADLIGHTS OFF', self)
        self.turn_off_headlights.resize(self.turn_off_headlights.sizeHint())
        self.turn_off_headlights.move(x, y + 25)
        self.turn_off_headlights.setToolTip('Turn off headlights')
        self.turn_off_headlights.clicked.connect(self.turn_lights_off)
        self.turn_off_headlights.show()

    def set_directions(self):
        """set_directions

        :return:
        """
        spi_cmd_id = chr(2)
        spi_data_0 = chr(int(self.motor_direction_holder[0].text()))
        spi_data_1 = chr(int(self.motor_direction_holder[1].text()))
        spi_data_2 = chr(int(self.motor_direction_holder[2].text()))
        spi_data_3 = chr(int(self.motor_direction_holder[3].text()))
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def set_power(self):
        """set_power

        :return:
        """
        spi_cmd_id = chr(1)
        spi_data_0 = chr(int(self.motor_power_holder[0].text()))
        spi_data_1 = chr(int(self.motor_power_holder[1].text()))
        spi_data_2 = chr(int(self.motor_power_holder[2].text()))
        spi_data_3 = chr(int(self.motor_power_holder[3].text()))
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def set_motor_control(self):
        """set_motor_control

        :return:
        """
        self.set_directions()
        sleep(0.005)
        self.set_power()

    def __lw_spi_data_entry__(self):
        """__lw_spi_data_entry__

            Load line edit entry used to send spi data to Crawler.
        :return:
        """
        self.spi_data_holder = [None] * 5
        for _ in range(5):
            self.spi_data_holder[_] = QLineEdit(self)
            self.spi_data_holder[_].move(20 + _ * 60, 145)
            self.spi_data_holder[_].resize(50, 20)
            self.spi_data_holder[_].show()


    def __lw_power_data_entry__(self):
        """__lw_power_data_entry__

            Load line edit entry used to send motors' power over spi data to Crawler.
        :return:
        """
        x = 20
        y = 260
        self.motor_power_holder = [None] * 5
        for _ in range(5):
            self.motor_power_holder[_] = QLineEdit(self)
            self.motor_power_holder[_].move(x + _ * 60, y)
            self.motor_power_holder[_].resize(50, 20)
            self.motor_power_holder[_].show()
        self.set_all_power_button = QPushButton('SAME POWER', self)
        self.set_all_power_button.resize(self.set_all_power_button.sizeHint())
        self.set_all_power_button.move(x + _ * 60, y - 25)
        self.set_all_power_button.setToolTip('Connect to Crawler')
        self.set_all_power_button.clicked.connect(self.__all_same_power__)
        self.set_all_power_button.show()

        self.motor_power_holder[-1].resize(self.set_all_power_button.size())
        
    def __lw_direction_data_entry__(self):
        """__lw_direction_data_entry__

            Load line edit entry used to send motors' direction over spi data to Crawler.
        :return:
        """
        x = 20
        y = 320
        self.motor_direction_holder = [None] * 5
        for _ in range(5):
            self.motor_direction_holder[_] = QLineEdit(self)
            self.motor_direction_holder[_].move(x + _ * 60, y)
            self.motor_direction_holder[_].resize(50, 20)
            self.motor_direction_holder[_].show()
        self.set_all_directions_button = QPushButton('SAME DIRECTIONS', self)
        self.set_all_directions_button.resize(self.set_all_directions_button.sizeHint())
        self.set_all_directions_button.move(x + _ * 60, y - 25)
        self.set_all_directions_button.setToolTip('Connect to Crawler')
        self.set_all_directions_button.clicked.connect(self.__all_same_direction__)
        self.set_all_directions_button.show()

        self.motor_direction_holder[-1].resize(self.set_all_directions_button.size())

    def __all_same_power__(self):
        """

        :return:
        """
        text = self.motor_power_holder[-1].text()
        for _ in self.motor_power_holder:
            _.setText(text)

    def __all_same_direction__(self):
        """

        :return:
        """
        text = self.motor_direction_holder[-1].text()
        for _ in self.motor_direction_holder:
            _.setText(text)

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

    def __lw_send_udp_button__(self):
        """__lw_send_udp_button__

            Load button used to send udp data to Crawler.
        :return: None
        """
        self.send_upd_button = QPushButton('SEND UDP DATA', self)
        self.send_upd_button.resize(self.send_upd_button.sizeHint())
        self.send_upd_button.move(20, 70)
        self.send_upd_button.setToolTip('send to Crawler')
        self.send_upd_button.clicked.connect(self.send_data_and_await_response)
        self.send_upd_button.show()

    def __lw_send_spi_button__(self):
        """__lw_send_spi_button__

            Load button used to send spi data to Crawler.
        :return: None
        """
        self.send_spi_button = QPushButton('SEND SPI DATA', self)
        self.send_spi_button.resize(self.send_spi_button.sizeHint())
        self.send_spi_button.move(20, 120)
        self.send_spi_button.setToolTip('send to Crawler')
        self.send_spi_button.clicked.connect(self.send_spi_data)
        self.send_spi_button.show()

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

        :return: 
        """
        data = self.udp_data_entry.text()
        response = self.__connection__.send_package_and_get_response(data)
        LOGGER.info(response)

    def set_direction_forward(self):
        """set_direction_forward

        :return:
        """
        spi_cmd_id = chr(2)
        spi_data_0 = chr(1)
        spi_data_1 = chr(1)
        spi_data_2 = chr(1)
        spi_data_3 = chr(1)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def set_direction_backward(self):
        """set_direction_backward

        :return:
        """
        spi_cmd_id = chr(2)
        spi_data_0 = chr(2)
        spi_data_1 = chr(2)
        spi_data_2 = chr(2)
        spi_data_3 = chr(2)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def stop_motors(self):
        """stop_motors

        :return:
        """
        spi_cmd_id = chr(2)
        spi_data_0 = chr(0)
        spi_data_1 = chr(0)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

        sleep(.005)

        spi_cmd_id = chr(1)
        spi_data_0 = chr(0)
        spi_data_1 = chr(0)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        
    def turn_lights_on(self):
        """turn_lights_on
        
        :return: 
        """

        spi_cmd_id = chr(3)
        spi_data_0 = chr(1)
        spi_data_1 = chr(1)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        
    def turn_lights_off(self):
        """turn_lights_off
        
        :return: 
        """

        spi_cmd_id = chr(3)
        spi_data_0 = chr(0)
        spi_data_1 = chr(0)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        
    def set_power_(self):
        """

        :return:
        """
        spi_cmd_id = chr(1)
        spi_data_0 = chr(int(self.spi_data_holder[1].text()))
        spi_data_1 = chr(int(self.spi_data_holder[2].text()))
        spi_data_2 = chr(int(self.spi_data_holder[3].text()))
        spi_data_3 = chr(int(self.spi_data_holder[4].text()))

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        
    def send_spi_data(self):
        """

        :return:
        """
        LOGGER.info("Sending SPI data")
        spi_cmd_id = chr(int(self.spi_data_holder[0].text()))
        spi_data_0 = chr(int(self.spi_data_holder[1].text()))
        spi_data_1 = chr(int(self.spi_data_holder[2].text()))
        spi_data_2 = chr(int(self.spi_data_holder[3].text()))
        spi_data_3 = chr(int(self.spi_data_holder[4].text()))

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def keyPressEvent(self, e):
        return

        spi_cmd_id = chr(2)
        spi_data_0 = chr(1)
        spi_data_1 = chr(1)
        spi_data_2 = chr(1)
        spi_data_3 = chr(1)

        key_pressed = e.key()
        if key_pressed == Qt.Key_W:
            spi_cmd_id = chr(2)
            spi_data_0 = chr(1)
            spi_data_1 = chr(1)
            spi_data_2 = chr(1)
            spi_data_3 = chr(1)
            
        elif key_pressed == Qt.Key_S:
            spi_cmd_id = chr(2)
            spi_data_0 = chr(2)
            spi_data_1 = chr(2)
            spi_data_2 = chr(2)
            spi_data_3 = chr(2)
            
        elif key_pressed == Qt.Key_A:
            spi_cmd_id = chr(2)
            spi_data_0 = chr(2)
            spi_data_1 = chr(1)
            spi_data_2 = chr(2)
            spi_data_3 = chr(1)
            
        elif key_pressed == Qt.Key_D:
            spi_cmd_id = chr(2)
            spi_data_0 = chr(1)
            spi_data_1 = chr(2)
            spi_data_2 = chr(1)
            spi_data_3 = chr(2)
            
        elif key_pressed == Qt.Key_Z:
            spi_cmd_id = chr(2)
            spi_data_0 = chr(0)
            spi_data_1 = chr(0)
            spi_data_2 = chr(0)
            spi_data_3 = chr(0)

        elif key_pressed == Qt.Key_P:
            spi_cmd_id = chr(1)
            spi_data_0 = chr(75)
            spi_data_1 = chr(75)
            spi_data_2 = chr(75)
            spi_data_3 = chr(75)

        elif key_pressed == Qt.Key_O:
            spi_cmd_id = chr(1)
            spi_data_0 = chr(0)
            spi_data_1 = chr(0)
            spi_data_2 = chr(0)
            spi_data_3 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrawlerGUI()

    sys.exit(app.exec_())
