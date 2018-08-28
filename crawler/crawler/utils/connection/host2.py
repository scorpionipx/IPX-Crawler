import logging
import threading
import socket as py_socket

from crawler.utils.connection.settings import *
from crawler.utils.connection.utils import get_local_machine_ip_addresses

LOGGER = logging.getLogger('crawler')
LOGGER.setLevel(logging.INFO)


class Host:
    """Host

        Class used to handle Crawler's server application.
    """
    def __init__(self, ip, port):
        """Constructor

        :param ip: Crawler's server IP address
        :type ip: str
        :param port: Crawler's communication port
        :type port: int
        """
        self.__ip__ = ip
        self.__port__ = port

        self.__connection__ = None
        self.__client__ = None

        self.server_is_on = False
        self.echo_mode_on = False

    def start_server(self):
        """start_server

            Start Crawler's server.
        :return: starting server result
        :rtype: bool
        """
        LOGGER.info("Starting Crawler's server...")
        try:
            self.__connection__ = py_socket.socket(py_socket.AF_INET, py_socket.SOCK_STREAM)
            self.__connection__.bind((py_socket.gethostname(), self.__port__))
        except Exception as err:
            error = "Failed to start Crawler's server! {}".format(err)
            LOGGER.error(error)
            return False

        self.__connection__.listen(ALLOWED_CONNECTIONS)
        self.server_is_on = True

        machine_ips = get_local_machine_ip_addresses()
        if len(machine_ips) > 0:
            LOGGER.info("Crawler's server is running and waiting for client connection!")
            LOGGER.info("HOSTNAME: {}".format(py_socket.gethostname()))

            for ip_index, machine_ip in enumerate(machine_ips):
                LOGGER.info("IP option #{}: {}".format(ip_index + 1, machine_ip))
            LOGGER.info("PORT: {}".format(self.__port__))
        else:
            LOGGER.info("Failed to retrieve local machine's IP address!")
            return False

        return True

    def stop_server(self):
        """stop_server

            Stop Crawler's server application
        :return: stopping server result
        :rtype: bool
        """
        LOGGER.info("Stopping Crawler's server...")
        try:
            self.__connection__.close()
        except Exception as err:
            error = "Failed to stop Crawler's server! {}".format(err)
            LOGGER.error(error)
            return False

        self.__connection__ = None
        self.server_is_on = False

        return True

    def __get_package_from_client__(self):
        """__get_package_from_client__

            Get a package from client.
        :return: package
        :rtype: bytearray
        """
        package = self.__client__.recv(BUFFER_SIZE)
        return package

    def echo(self):
        """echo

            Run server in echo mode.
        :return: None
        """
        if self.__client__ is None:
            self.connect_with_client()

        package_income_thread = threading.Thread(target=self.__echo__)
        self.echo_mode_on = True
        package_income_thread.start()
        package_income_thread.join()

    def __echo__(self):
        """__echo__

            Thread echo.
        :return: None
        """
        lost_connection_packages_counter = 0
        while self.echo_mode_on:
            incoming_package = self.__get_package_from_client__()

            decoded_package = incoming_package.decode(encoding=ENCODING)
            LOGGER.info("echo mode - received package: {} - {}".format(decoded_package, len(decoded_package)))

            if decoded_package == LOST_CONNECTION_PACKAGE:
                LOGGER.info("echo mode - received null package")
                lost_connection_packages_counter += 1

                if lost_connection_packages_counter >= LOST_CONNECTION_PACKAGES_LIMIT:
                    LOGGER.info("Number of null packages received exceeded limit of {}!"
                                .format(LOST_CONNECTION_PACKAGES_LIMIT))
                    self.stop_echo()

                continue

            if 'stop echo' in decoded_package:
                self.stop_echo()

    def stop_echo(self):
        """echo

            Stop echo mode.
        :return: None
        """
        self.echo_mode_on = False
        LOGGER.info("Stopped echo mode!")

    def connect_with_client(self):
        """connect_with_client

            Connects with a requesting client.
        :return: None
        """
        client_is_valid = False

        LOGGER.info("Waiting for connection request...")
        while not client_is_valid:

            # establish a connection
            self.__client__, client_address = self.__connection__.accept()
            LOGGER.info("Got a connection request from {}".format(str(client_address[0])))

            client_is_valid = True
            LOGGER.info("Connected to {}!".format(client_address))

            if client_is_valid:
                pass
            else:
                LOGGER.info("Unknown client connection request! Connection refused!")
                self.__client__.shutdown(py_socket.SHUT_RDWR)
                self.__client__.close()
                self.__client__ = None


if __name__ == '__main__':
    h = Host(DEFAULT_IP, DEFAULT_PORT)
    h.start_server()
    assert h.server_is_on
    h.echo()
    h.stop_server()
    assert not h.server_is_on
