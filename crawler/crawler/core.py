import logging

from crawler.utils.connection.host import Host
from crawler.utils.connection.settings import DEFAULT_PORT

logger = logging.getLogger('ipx_logger')


class Crawler:
    """Crawler
        Class used to handle remote controlled device.
    """
    def __init__(self, ip=None, port=DEFAULT_PORT):
        """Constructor
        """
        logger.debug("Initializing Crawler...")
        print("ip: {}".format(ip))
        self.connection = Host(forced_ip=ip, port=port)

        self.__listening__ = False
        logger.debug("Crawler initialized!")

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
        self.connection.run_echo_mode()

    def speak(self, text):
        """speak
            Speak provided speech.
        :param text: text to be spoken as string.
        :return: None
        """
        pass


