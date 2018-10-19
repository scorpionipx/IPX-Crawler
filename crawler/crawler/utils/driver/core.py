import logging
import spidev

from crawler.version import __version__

LOGGER = logging.getLogger('crawler')
LOGGER.setLevel(logging.INFO)


class CrawlerDriverBoardSTM:
    """CrawlerDriverBoard

        Class used to handle Crawler's Driver Board.
    """
    def __init__(self):
        self.SPI = spidev.SpiDev()
        self.__init_SPI__()

    def __init_SPI__(self):
        """__init_SPI__

            Initialize SPI module
        :return: None
        """

        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 7800000

    def send_SPI_data(self, data):
        """send_SPI_data

            Send specified data over SPI module.
        :param data: data to be sent
        :type data: list
        :return: None
        """
        LOGGER.info("Sending SPI {}".format(len(data)))
        self.SPI.xfer(data)
