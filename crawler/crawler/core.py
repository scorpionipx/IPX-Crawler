import logging
import pygame
import threading

from time import sleep

from crawler.utils.connection.host2 import Host
from crawler.utils.connection.settings import DEFAULT_PORT

from crawler.utils.driver.core import CrawlerDriverBoardSTM
from crawler.utils.voice import speak, LANGUAGE_LITERAL


JOYSTICK_X_AXIS = 0
JOYSTICK_Y_AXIS = 3
JOYSTICK_HEADLIGHTS_BUTTON = 6
JOYSTICK_CAMERA_ROTATION_CCW_BUTTON = 8
JOYSTICK_CAMERA_ROTATION_CW_BUTTON = 9

NOB_TO_N = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3}


LOGGER = logging.getLogger('crawler')
LOGGER.setLevel(logging.INFO)


class Crawler:
    """Crawler
        Class used to handle remote controlled device.
    """
    def __init__(self, ip=None, port=DEFAULT_PORT, manual_control=False):
        """Constructor
        """
        LOGGER.debug("Initializing Crawler...")
        self.lights_on = False
        if manual_control:
            global JOYSTICK_HEADLIGHTS_BUTTON
            global JOYSTICK_CAMERA_ROTATION_CCW_BUTTON
            global JOYSTICK_CAMERA_ROTATION_CW_BUTTON
            global JOYSTICK_X_AXIS
            global JOYSTICK_Y_AXIS

            pygame.init()
            pygame.joystick.init()

            joystick_count = pygame.joystick.get_count()
            if joystick_count > 0:
                self.manual_control = True
                self.joystick = pygame.joystick.Joystick(0)
                self.joystick.init()
                joystick_name = self.joystick.get_name()
                LOGGER.info("JOYSTICK FOUND: {}".format(joystick_name))
                if 'Controller' in joystick_name:
                    JOYSTICK_HEADLIGHTS_BUTTON = 2
                    JOYSTICK_CAMERA_ROTATION_CCW_BUTTON = 4
                    JOYSTICK_CAMERA_ROTATION_CW_BUTTON = 5
                    JOYSTICK_X_AXIS = 0
                    JOYSTICK_Y_AXIS = 4

                sleep(0.5)
                axes = self.joystick.get_numaxes()
                LOGGER.info(axes)

                axis_thread = threading.Thread(target=self.__manual_control__)
                axis_thread.start()
            else:
                LOGGER.info("No joystick device connected!")
        else:
            print("ip: {}".format(ip))
            self.connection = Host(ip=ip, port=port)
        self.driver = CrawlerDriverBoardSTM()

        self.__listening__ = False
        LOGGER.debug("Crawler initialized!")

    def stop_manual_control(self):
        """stop_manual_control

        :return:
        """
        self.manual_control = False

    def build_spi_command(self, cmd_id, data):
        """build_spi_command

            Build SPI command.
        :param cmd_id: command's ID in range [0, 31]
        :type cmd_id: int
        :param data: list of 8 bits data to be sent, maximum 1024 bytes
        :type data: list of int
        :return: None
        """
        number_of_data_bytes = len(data)

        if number_of_data_bytes <= 7:
            extend = 0
            n = NOB_TO_N[number_of_data_bytes + 1]
            data_0_byte = False
            frame_length = 1 << n
        else:
            number_of_data_bytes += 1
            extend = 1
            n = (number_of_data_bytes & 0b1100000000) >> 8
            data_0_byte = number_of_data_bytes & 0xFF
            data_frame_length = number_of_data_bytes + 1
            frame_length = data_frame_length + 1

        # LOGGER.info("FRAME L: {}".format(frame_length))
        header_byte = (cmd_id << 3) | (extend << 2) | n

        spi_data = [header_byte]

        if data_0_byte:
            spi_data.append(data_0_byte)

        spi_data.extend(data)
        if extend == 0:
            while len(spi_data) < frame_length:
                spi_data.append(0)

        # for spi_byte in spi_data:
        #     LOGGER.info("{0:08b}: {1} {2}".format(spi_byte, spi_byte, chr(spi_byte)))

        return spi_data

    def __manual_control__(self):
        """__manual_control__

        :return:
        """
        number_of_buttons = self.joystick.get_numbuttons()
        LOGGER.info("{} buttons".format(number_of_buttons))
        button_pressed = [False] * number_of_buttons
        button_allowed = [True] * number_of_buttons
        button_forbidden_cycles = 3
        button_allowed_counter = [button_forbidden_cycles] * number_of_buttons
        spi_delay = 0.05
        no_need_to_send_counter = 0
        no_need_to_send = False

        while self.manual_control:
            pygame.event.pump()
            x = int(self.joystick.get_axis(JOYSTICK_X_AXIS) * 100)
            y = - int(self.joystick.get_axis(JOYSTICK_Y_AXIS) * 100)

            for i in range(6):
                axis = self.joystick.get_axis(i)
                if axis:
                    LOGGER.info("AXIS {}".format(i))

            for button_index in range(number_of_buttons):
                if self.joystick.get_button(button_index):
                    button_pressed[button_index] = True
                    LOGGER.info("Button {}".format(button_index))

            if button_pressed[JOYSTICK_HEADLIGHTS_BUTTON] and button_allowed[JOYSTICK_HEADLIGHTS_BUTTON]:
                button_pressed[JOYSTICK_HEADLIGHTS_BUTTON] = False
                button_allowed[JOYSTICK_HEADLIGHTS_BUTTON] = False
                if self.lights_on:
                    self.turn_lights_off()
                else:
                    self.turn_lights_on()
                sleep(spi_delay)

            if not button_allowed[JOYSTICK_HEADLIGHTS_BUTTON]:
                button_allowed_counter[JOYSTICK_HEADLIGHTS_BUTTON] -= 1
                if button_allowed_counter[JOYSTICK_HEADLIGHTS_BUTTON] == 0:
                    button_allowed_counter[JOYSTICK_HEADLIGHTS_BUTTON] = button_forbidden_cycles
                    button_allowed[JOYSTICK_HEADLIGHTS_BUTTON] = True

            if button_pressed[JOYSTICK_CAMERA_ROTATION_CCW_BUTTON]:
                button_pressed[JOYSTICK_CAMERA_ROTATION_CCW_BUTTON] = False
                button_pressed[JOYSTICK_CAMERA_ROTATION_CW_BUTTON] = False
                self.rotate_camera_ccw()
                sleep(spi_delay)

            if button_pressed[JOYSTICK_CAMERA_ROTATION_CW_BUTTON]:
                button_pressed[JOYSTICK_CAMERA_ROTATION_CCW_BUTTON] = False
                button_pressed[JOYSTICK_CAMERA_ROTATION_CW_BUTTON] = False
                self.rotate_camera_cw()
                sleep(spi_delay)

            if x == 0 == y:
                no_need_to_send_counter += 1
                if no_need_to_send_counter > 3:
                    no_need_to_send = True
            else:
                no_need_to_send_counter = 0
                no_need_to_send = False

            if no_need_to_send:
                continue

            l_pwm = 0
            r_pwm = 0

            if x >= 0 and y > 0:
                l_pwm = y
                r_pwm = y - x
            elif x < 0 and y > 0:
                l_pwm = y + x
                r_pwm = y
            elif x >= 0 and y < 0:
                l_pwm = y
                r_pwm = y + x
            elif x < 0 and y < 0:
                l_pwm = y - x
                r_pwm = y
            elif x >= 0 and y == 0:
                l_pwm = x
                r_pwm = -x

            elif x <= 0 and y == 0:
                l_pwm = x
                r_pwm = -x

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

            directions = l_dir
            directions <<= 2
            directions |= r_dir

            if l_pwm < 0:
                l_pwm = - l_pwm
            if r_pwm < 0:
                r_pwm = - r_pwm

            drive_spi_data = self.build_spi_command(cmd_id=10, data=[l_pwm, r_pwm, directions])
            # LOGGER.info(drive_spi_data)
            self.driver.send_spi_data(drive_spi_data)
            sleep(spi_delay)

    def connect_with_client(self):
        """connect_with_client
            Connect with a client.
        :return: None
        """
        self.connection.connect_with_client()

    def echo(self):
        """echo
            Crawler echos back every data income from controller.
        :return: None
        """
        self.connection.echo()

    def turn_lights_on(self):
        """turn_lights_on

        :return:
        """
        spi_data = self.build_spi_command(cmd_id=3, data=[3])
        # LOGGER.info(drive_spi_data)
        self.driver.send_spi_data(spi_data)
        self.lights_on = True

    def turn_lights_off(self):
        """turn_lights_off

        :return:
        """
        spi_data = self.build_spi_command(cmd_id=3, data=[0])
        # LOGGER.info(drive_spi_data)
        self.driver.send_spi_data(spi_data)
        self.lights_on = False

    def rotate_camera_ccw(self):
        """rotate_camera_ccw

        :return:
        """
        spi_data = self.build_spi_command(cmd_id=5, data=[1])
        # LOGGER.info(drive_spi_data)
        self.driver.send_spi_data(spi_data)

    def rotate_camera_cw(self):
        """rotate_camera_cw

        :return:
        """
        spi_data = self.build_spi_command(cmd_id=5, data=[2])
        # LOGGER.info(drive_spi_data)
        self.driver.send_spi_data(spi_data)

    def listen(self):
        """listen

            Listen to incoming ethernet packages and execute commands.
        :return: 
        """
        listen_thread = threading.Thread(target=self.__listen__)
        listen_thread.start()

    def __listen__(self):
        """__listen__
        
            Listen to incoming ethernet packages and execute commands thread.
        :return: None
        """
        if not self.connection.server_is_on:
            self.connection.start_server()

        if self.connection.__client__ is None:
            self.connection.connect_with_client()

        self.connection.listening = True

        while self.connection.listening:
            incoming_package = self.connection.__get_package_from_client__()
            # LOGGER.info(incoming_package)
            decoded_package = incoming_package.decode('utf-8')

            if 'spi' in decoded_package:
                self.driver.send_spi_data([1, 50, 50, 50, 50, 50])
            self.connection.send_package(decoded_package)

            if 'stop_listening' in decoded_package:
                self.connection.stop_listening()

            if '$i' in decoded_package:
                if '$d' in decoded_package:
                    self.decode_command(decoded_package)
        
    def speak(self, speak_data):
        """speak

            Speak provided speech.
        :param speak_data: 
        :return: 
        """
        speak_thread = threading.Thread(target=self.__speak__, args=(speak_data, ))
        speak_thread.start()

    def __speak__(self, speak_data):
        """__speak__

        :param speak_data:
        :type speak_data: str
        :return:
        """
        words = speak_data[:speak_data.find(LANGUAGE_LITERAL)]
        lang = speak_data[speak_data.find(LANGUAGE_LITERAL) + len(LANGUAGE_LITERAL):]
        speak(speech=words, language=lang)

    def decode_command(self, package):
        """decode_command

            Transform UDP data to Crawler command.
        :param package: package received from client
        :type package: str
        :return:
        """
        cmd_id = package[package.find("$i") + 2:package.find("$d")]
        data = package[package.find("$d") + 2:]

        try:
            cmd_id = int(cmd_id)
            if cmd_id == 50:
                spi_data = []
                for char in data:
                    spi_data.append(ord(char))

                # LOGGER.info("SPI DATA RECEIVED: {}, type {}".format(spi_data, type(spi_data)))
                # for spi_d in spi_data:
                    # LOGGER.info("DATA: {}".format(spi_d))

                self.driver.send_spi_data(spi_data)
            elif cmd_id == 51:
                LOGGER.info("SPEECH DATA: {}".format(data))
                self.speak(data)

        except Exception as err:
            LOGGER.info(err)
            pass

        LOGGER.info("CMD_ID: {}".format(cmd_id))
        LOGGER.info("DATA: {}".format(data))





