import spidev


class CrawlerDriverBoardSTM:
    """CrawlerDriverBoard

        Class used to handle Crawler's Driver Board.
    """
    def __init__(self):
        self.SPI = spidev.SpiDev()

    def __init_SPI__(self):
        """__init_SPI__

            Initialize SPI module
        :return: None
        """
        self.SPI.open(0, 0)
        self.SPI.max_speed_hz = 61000

    def send_SPI_DATA(self, data):
        """send_SPI_DATA

            Send specified data over SPI module.
        :param data: data to be sent
        :type data: int
        :return: None
        """
        self.SPI.xfer([data])
