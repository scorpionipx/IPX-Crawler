import logging
import socket as py_socket

from crawler.utils.connection.settings import *

logger = logging.getLogger('ipx_logger')


class Host:
    """Host
        Class used to handle internet connection on the crawler as host(slave).
    """

    def __init__(self, forced_ip=None, port=DEFAULT_PORT, number_of_connections=DEFAULT_ALLOWED_CONNECTIONS):
        """
            Constructor
        :param port: host's communication port as integer
                     example: 1369
        :param number_of_connections: host's maximum number of connection allowed at once
                                      example: 1
        """
        try:
            logger.debug("Initiating host...")

            # create the socket object
            self.socket = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)

            # set host's name
            self.name = py_socket.gethostname()

            # set host's ip address and port
            if forced_ip is None:
                self.ip = self.__get_host_ip_address__()
            else:
                self.ip = forced_ip
            self.port = port

            # bind the socket to public interface
            if forced_ip is None:
                self.socket.bind((self.name, self.port))
            else:
                self.socket.bind((forced_ip, self.port))
            logger.debug("{}, {}, {}".format(self.name, self.ip, self.port))

            # allow a specific number of connections
            self.socket.listen(number_of_connections)

            # client instance and attributes
            self.client = None

            # connection encoding
            self.encoding = 'utf-8'

            logger.debug("Host initiated!")

        except Exception as err:
            error = 'Failed to initialize host! ' + str(err)
            logger.error(error)

    def __get_host_ip_address__(self):
        """
            Get current created host's ip address.
        At initialization, IP address is unknown. It may be different when connected to another router/network.
        Host's IP address is needed by client to know at which address to connect.
        :return: ip - string
        """
        ip = py_socket.gethostbyname(py_socket.gethostname())
        return ip

    def get_ip(self):
        """
            Get host's ip address.
        :return: ip - string
        """
        return self.ip

    def get_port(self):
        """
            Get host's port.
        :return: port - integer
        """
        return self.port

    def get_name(self):
        """
            Get host's name.
        :return: name - string
        """
        return self.name

    def get_encoding(self):
        """
            Get host's encoding.
        :return: encoding - string
        """
        return self.encoding

    def get_info(self):
        """
            Get host's info: ip address, port, name, encoding, etc...
        :return: host_info - string
        """

        name = self.get_name()
        ip = self.get_ip()
        port = self.get_port()
        encoding = self.get_encoding()

        host_info = "Host info\n"
        host_info += "Name: " + str(name) + "\n"
        host_info += "IP: " + str(ip) + "\n"
        host_info += "Port: " + str(port) + "\n"
        host_info += "Encoding: " + str(encoding) + "\n"

        return host_info

    def string_to_bytes(self, _string, encoding=None):
        """
            Method converts string type to bytes, using specified encoding.
        Conversion is required for socket's data transfer protocol: string type is not supported.
        :param _string: string to be converted
        :param encoding: character encoding key
        :return: bytes(_string, encoding)
        """
        if encoding is None:
            encoding = self.encoding
        return bytes(_string, encoding)

    def connect_with_client(self):
        """
            Connects with a connection requesting client.
        :return: None
        """
        client_is_valid = False

        logger.info("Waiting for connection request at IP: {}".format(py_socket.gethostbyname(py_socket.gethostname())))
        while not client_is_valid:

            # establish a connection
            self.client, client_address = self.socket.accept()
            logger.info("Got a connection request from " + str(client_address[0]))

            client_is_valid = True
            logger.info("Connected to {}!".format(client_address))

            if client_is_valid:
                pass
            else:
                logger.info("Unknown client connection request! Connection refused!")
                self.client.shutdown(py_socket.SHUT_RDWR)
                self.client.close()
                self.client = None

    def get_package_from_client(self):
        """get_package_from_client
            Get a package from client.
        :return: package
        """
        package = self.client.recv(DEFAULT_BUFFER_SIZE)
        return package

    def run_echo_mode(self):
        """run_echo_mode
            Server continuously receives data from client and echos it back
        :return: None
        """
        if self.client is None:
            self.connect_with_client()
        logger.debug("Echo mode enabled! Waiting for client's data...")

        echo_mode = True
        invalid_data_counter = 0
        MAX_INVALID_DATA = 500

        while echo_mode:
            data_from_client = self.get_package_from_client().decode(self.encoding)

            if data_from_client is None:
                invalid_data_counter += 1
            else:
                invalid_data_counter = 0

            if invalid_data_counter >= MAX_INVALID_DATA:
                logger.info("Echo mode stopped! Maximum invalid data received from client reached! [{}]".
                            format(MAX_INVALID_DATA))
                echo_mode = False

            logger.debug("Received package from host: {}".format(data_from_client))

            self.client.send(bytes(data_from_client, self.encoding))

            if data_from_client == "exit":
                echo_mode = False


