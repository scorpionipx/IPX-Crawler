import logging
import threading

from crawler.utils.connection.host2 import Host
from crawler.utils.connection.settings import DEFAULT_PORT

from crawler.utils.driver.core import CrawlerDriverBoardSTM

LOGGER = logging.getLogger('crawler')
LOGGER.setLevel(logging.INFO)


class Crawler:
    """Crawler
        Class used to handle remote controlled device.
    """
    def __init__(self, ip=None, port=DEFAULT_PORT):
        """Constructor
        """
        LOGGER.debug("Initializing Crawler...")
        print("ip: {}".format(ip))
        self.connection = Host(ip=ip, port=port)
        self.driver = CrawlerDriverBoardSTM()

        self.__listening__ = False
        LOGGER.debug("Crawler initialized!")

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
            LOGGER.info(incoming_package)
            decoded_package = incoming_package.decode('utf-8')

            if 'spi' in decoded_package:
                self.driver.send_SPI_data([1, 50, 50, 50, 50])
            self.connection.send_package(decoded_package)

            if 'stop_listening' in decoded_package:
                self.connection.stop_listening()

    def speak(self, text):
        """speak
            Speak provided speech.
        :param text: text to be spoken as string.
        :return: None
        """
        pass


