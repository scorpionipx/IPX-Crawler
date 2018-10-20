from crawler.version import __version__
import logging

LOGGER = logging.getLogger('crawler')
LOGGER.setLevel(logging.INFO)


def send_spi_command(cmd_id, data):
    """send_spi_command

        Send SPI command.
    :param cmd_id: command's ID in range [0, 31]
    :type cmd_id: int
    :param data: list of 8 bits data to be sent, maximum 1024 bytes
    :type data: list of int
    :return: None
    """
    NOB_TO_N = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 3, 8: 3}
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

    LOGGER.info("FRAME L: {}".format(frame_length))
    header_byte = (cmd_id << 3) | (extend << 2) | n

    spi_data = [header_byte]

    if data_0_byte:
        spi_data.append(data_0_byte)

    spi_data.extend(data)
    if extend == 0:
        while len(spi_data) < frame_length:
            spi_data.append(0)

    for spi_byte in spi_data:
        LOGGER.info("{0:08b}: {1} {2}".format(spi_byte, spi_byte, chr(spi_byte)))

    return spi_data


if __name__ == "__main__":
    cmd_id = 4
    text = "ScorpionIPX"
    ascii = [ord(x) for x in text]
    LOGGER.info(ascii)
    spi_data = ascii
    spi_data = [100, 90, 0b01010101]

    send_spi_command(cmd_id, spi_data)

