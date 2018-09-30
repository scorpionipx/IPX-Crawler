import spidev


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
        self.SPI.max_speed_hz = 5000000

    def send_SPI_data(self, data):
        """send_SPI_data

            Send specified data over SPI module.
        :param data: data to be sent
        :type data: list
        :return: None
        """
        self.SPI.xfer(data)
