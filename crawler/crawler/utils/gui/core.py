from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget, QTextEdit, QPushButton, QInputDialog, QLineEdit, \
    QComboBox, QMessageBox, QLabel

from PyQt5.QtCore import Qt

from crawler.utils.gui.utils import DragButton

import logging
import os.path
import sys
import threading

from time import sleep

from crawler.version import __version__
from crawler.utils.connection.client import Client
import pygame


LOGGER = logging.getLogger('crawler')
LOGGER.level = logging.INFO

APP_TITLE = 'CrawlerIPX'
APP_SIZE_WIDTH = 800
APP_SIZE_HEIGHT = 600

CURRENT_DIR = os.path.dirname(__file__)
LANGUAGE_LITERAL = 'ipx_lang:'

JOYSTICK_X_AXIS = 0
JOYSTICK_Y_AXIS = 0
JOYSTICK_HEADLIGHTS_BUTTON = 6


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

        self.manual_control = False
        self.joystick = None
        self.x_axis = None
        self.y_axis = None

        self.lights_on = False

        super().__init__()

        self.init_gui()
        self.init_joystick()

    def init_joystick(self):
        """

        :return:
        """
        pygame.init()
        pygame.joystick.init()

        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            self.manual_control = True
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            LOGGER.info("JOYSTICK FOUND: {}".format(self.joystick.get_name()))
            sleep(0.5)
            axes = self.joystick.get_numaxes()
            LOGGER.info(axes)

            axis_thread = threading.Thread(target=self.__get_axis__)
            axis_thread.start()
        else:
            LOGGER.info("No joystick device connected!")

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.manual_control = False
            event.accept()
        else:
            event.ignore()

    def __get_axis__(self):
        """__get_axis__

        :return:
        """
        number_of_buttons = self.joystick.get_numbuttons()
        LOGGER.info("{} buttons".format(number_of_buttons))
        button_pressed = [False] * number_of_buttons
        spi_delay = 0.1

        while self.manual_control:

            pygame.event.pump()
            x = int(self.joystick.get_axis(0) * 100)
            y = - int(self.joystick.get_axis(3) * 100)

            for button_index in range(number_of_buttons):
                if self.joystick.get_button(button_index):
                    button_pressed[button_index] = True
                    LOGGER.info("Button {} pressed".format(button_index))

            if button_pressed[JOYSTICK_HEADLIGHTS_BUTTON]:
                button_pressed[JOYSTICK_HEADLIGHTS_BUTTON] = False
                if self.__connection__:
                    if self.lights_on:
                        self.turn_lights_off()
                    else:
                        self.turn_lights_on()
                    sleep(spi_delay)

            l_pwm = 0
            r_pwm = 0

            if x >= 0 and y > 0:
                l_pwm = y
                r_pwm = y - x
            elif x < 0 and y > 0:
                l_pwm = y + x
                r_pwm = y
            elif x >=0 and y < 0:
                l_pwm = y
                r_pwm = y + x
            elif x < 0 and y < 0:
                l_pwm = y - x
                r_pwm = y
            elif x >= 0 and y == 0:
                l_pwm = x
                r_pwm = -x

            elif x <= 0 and y == 0:
                l_pwm = -x
                r_pwm = x

            if l_pwm > 0:
                l_dir = 1
            elif l_pwm < 0:
                l_dir = 2
            else:
                l_dir = 0

            if r_pwm > 0:
                r_dir = 1
            elif r_pwm < 0:
                r_dir = 2
            else:
                r_dir = 0

            self.info_pwm_fl.setText(str(l_pwm))
            self.info_pwm_rl.setText(str(l_pwm))
            self.info_pwm_fr.setText(str(r_pwm))
            self.info_pwm_rr.setText(str(r_pwm))

            spi_cmd_id = chr(2)
            spi_data_0 = chr(l_dir)
            spi_data_1 = chr(r_dir)
            spi_data_2 = chr(l_dir)
            spi_data_3 = chr(r_dir)
            spi_data_4 = chr(0)
            udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
            if self.__connection__:
                pass
                response = self.__connection__.send_package_and_get_response(udp_frame)

            sleep(spi_delay)
        
            if l_pwm < 0:
                l_pwm = - l_pwm
            if r_pwm < 0:
                r_pwm = - r_pwm
        
            spi_cmd_id = chr(1)
            spi_data_0 = chr(l_pwm)
            spi_data_1 = chr(r_pwm)
            spi_data_2 = chr(l_pwm)
            spi_data_3 = chr(r_pwm)
            spi_data_4 = chr(0)
            udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
            if self.__connection__:
                pass
                response = self.__connection__.send_package_and_get_response(udp_frame)

            # LOGGER.info("{} - {}".format(self.x_axis, self.y_axis))
            sleep(spi_delay)

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

        self.__create_speech_line_edit__()
        self.__create_select_language_combobox__()
        self.__create_speak_button__()
        self.__lw_knob__()
        self.__lw_motors_info__()

    def __lw_motors_info__(self):
        """__lw_motors_info__

            Load widgets used to display info about motors.
        :return:
        """
        x = 500
        y = 400
        x_spacing = 50
        x_motor_offset = 14
        x_pwm_offset = 55
        x_dir_offset = 100
        y_spacing = 20

        header_motor = QLabel(self)
        header_motor.setText("MOTOR")
        header_motor.move(x, y)
        header_motor.resize(header_motor.sizeHint())
        header_motor.show()

        header_motor_fl = QLabel(self)
        header_motor_fl.setText("FL")
        header_motor_fl.move(x + x_motor_offset, y + y_spacing)
        header_motor_fl.resize(header_motor_fl.sizeHint())
        header_motor_fl.show()

        header_motor_fr = QLabel(self)
        header_motor_fr.setText("FR")
        header_motor_fr.move(x + x_motor_offset, y + 2 * y_spacing)
        header_motor_fr.resize(header_motor_fr.sizeHint())
        header_motor_fr.show()

        header_motor_rl = QLabel(self)
        header_motor_rl.setText("RL")
        header_motor_rl.move(x + x_motor_offset, y + 3 * y_spacing)
        header_motor_rl.resize(header_motor_rl.sizeHint())
        header_motor_rl.show()

        header_motor_rr = QLabel(self)
        header_motor_rr.setText("RR")
        header_motor_rr.move(x + x_motor_offset, y + 4 * y_spacing)
        header_motor_rr.resize(header_motor_rr.sizeHint())
        header_motor_rr.show()

        header_pwm = QLabel(self)
        header_pwm.setText("PWM")
        header_pwm.move(x + x_spacing, y)
        header_pwm.resize(header_pwm.sizeHint())
        header_pwm.show()

        self.info_pwm_fl = QLabel(self)
        self.info_pwm_fl.setText("000")
        self.info_pwm_fl.move(x + x_pwm_offset, y + y_spacing)
        self.info_pwm_fl.resize(self.info_pwm_fl.sizeHint())
        self.info_pwm_fl.show()

        self.info_pwm_fr = QLabel(self)
        self.info_pwm_fr.setText("000")
        self.info_pwm_fr.move(x + x_pwm_offset, y + 2 * y_spacing)
        self.info_pwm_fr.resize(self.info_pwm_fr.sizeHint())
        self.info_pwm_fr.show()

        self.info_pwm_rl = QLabel(self)
        self.info_pwm_rl.setText("000")
        self.info_pwm_rl.move(x + x_pwm_offset, y + 3 * y_spacing)
        self.info_pwm_rl.resize(self.info_pwm_rl.sizeHint())
        self.info_pwm_rl.show()

        self.info_pwm_rr = QLabel(self)
        self.info_pwm_rr.setText("000")
        self.info_pwm_rr.move(x + x_pwm_offset, y + 4 * y_spacing)
        self.info_pwm_rr.resize(self.info_pwm_rr.sizeHint())
        self.info_pwm_rr.show()

        header_dir = QLabel(self)
        header_dir.setText("DIR")
        header_dir.move(x + 2 * x_spacing, y)
        header_dir.resize(header_dir.sizeHint())
        header_dir.show()

        self.info_dir_fl = QLabel(self)
        self.info_dir_fl.setText("N/A")
        self.info_dir_fl.move(x + x_dir_offset, y + y_spacing)
        self.info_dir_fl.resize(self.info_dir_fl.sizeHint())
        self.info_dir_fl.show()

        self.info_dir_fr = QLabel(self)
        self.info_dir_fr.setText("N/A")
        self.info_dir_fr.move(x + x_dir_offset, y + 2 * y_spacing)
        self.info_dir_fr.resize(self.info_dir_fr.sizeHint())
        self.info_dir_fr.show()

        self.info_dir_rl = QLabel(self)
        self.info_dir_rl.setText("N/A")
        self.info_dir_rl.move(x + x_dir_offset, y + 3 * y_spacing)
        self.info_dir_rl.resize(self.info_dir_rl.sizeHint())
        self.info_dir_rl.show()

        self.info_dir_rr = QLabel(self)
        self.info_dir_rr.setText("N/A")
        self.info_dir_rr.move(x + x_dir_offset, y + 4 * y_spacing)
        self.info_dir_rr.resize(self.info_dir_rr.sizeHint())
        self.info_dir_rr.show()

    def __lw_knob__(self):
        """

        :return:
        """
        size = 16
        self.knob = DragButton(self)
        self.knob.move(500, 500)
        self.knob.resize(size, size)
        self.knob.show()

    def __create_speech_line_edit__(self):
        """__create_speech_line_edit__
            Create the line edit used to store as text the speech for Crawler.
        :return: None
        """
        x = 10
        y = 400
        self.speech_text_edit = QTextEdit(self)
        self.speech_text_edit.move(x, y)
        self.speech_text_edit.resize(400, 80)
        self.speech_text_edit.show()
        self.speech_text_edit.setText("Hello! I am Crawler!")

    def __create_select_language_combobox__(self):
        """__create_select_language_combobox__
            Creates the combobox used to select Crawler's speech language.
        :return: None
        """
        x = 10
        y = 490
        self.language_select_combobox = QComboBox(self)
        self.language_select_combobox.move(x, y)
        self.language_select_combobox.addItem('en')
        self.language_select_combobox.addItem('ro')
        self.language_select_combobox.show()

    def __create_speak_button__(self):
        """__create_speak_button__
            Creates the button used to tell Crawler to speak provided text.
        :return: None
        """
        x = 250
        y = 490
        self.speak_button = QPushButton(self)
        self.speak_button.move(x, y)
        self.speak_button.setText('Speak')
        self.speak_button.clicked.connect(self.speak)
        self.speak_button.show()
        
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

    def speak(self):
        """

        :return:
        """
        try:
            udp_frame = '$i51$d' + self.speech_text_edit.toPlainText() + LANGUAGE_LITERAL + \
                        str(self.language_select_combobox.currentText())
            response = self.__connection__.send_package_and_get_response(udp_frame)

            LOGGER.info(response)
        except Exception as err:
            LOGGER.info(err)

    def set_directions(self):
        """set_directions

        :return:
        """
        spi_cmd_id = chr(2)
        spi_data_0 = chr(int(self.motor_direction_holder[0].text()))
        spi_data_1 = chr(int(self.motor_direction_holder[1].text()))
        spi_data_2 = chr(int(self.motor_direction_holder[2].text()))
        spi_data_3 = chr(int(self.motor_direction_holder[3].text()))
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        number_of_spi_data_holders = 6
        self.spi_data_holder = [None] * number_of_spi_data_holders
        for _ in range(number_of_spi_data_holders):
            self.spi_data_holder[_] = QLineEdit(self)
            self.spi_data_holder[_].move(20 + _ * 60, 145)
            self.spi_data_holder[_].resize(50, 20)
            self.spi_data_holder[_].show()
            self.spi_data_holder[_].setText("0")


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
            self.motor_power_holder[_].setText("0")

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
            self.motor_direction_holder[_].setText("0")

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
        self.udp_data_entry.setText("udp frame")

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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

        sleep(.005)

        spi_cmd_id = chr(1)
        spi_data_0 = chr(0)
        spi_data_1 = chr(0)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        self.lights_on = True
        
    def turn_lights_off(self):
        """turn_lights_off
        
        :return: 
        """

        spi_cmd_id = chr(3)
        spi_data_0 = chr(0)
        spi_data_1 = chr(0)
        spi_data_2 = chr(0)
        spi_data_3 = chr(0)
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)
        self.lights_on = False
        
    def set_power_(self):
        """

        :return:
        """
        spi_cmd_id = chr(1)
        spi_data_0 = chr(int(self.spi_data_holder[1].text()))
        spi_data_1 = chr(int(self.spi_data_holder[2].text()))
        spi_data_2 = chr(int(self.spi_data_holder[3].text()))
        spi_data_3 = chr(int(self.spi_data_holder[4].text()))
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
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
        spi_data_4 = chr(0)

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)

    def keyPressEvent(self, e):
        return

        spi_cmd_id = chr(2)
        spi_data_0 = chr(1)
        spi_data_1 = chr(1)
        spi_data_2 = chr(1)
        spi_data_3 = chr(1)
        spi_data_4 = chr(0)

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

        udp_frame = '$i50$d' + spi_cmd_id + spi_data_0 + spi_data_1 + spi_data_2 + spi_data_3 + spi_data_4
        response = self.__connection__.send_package_and_get_response(udp_frame)
        LOGGER.info(response)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CrawlerGUI()

    sys.exit(app.exec_())
