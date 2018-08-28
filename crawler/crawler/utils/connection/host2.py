import logging
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
        try:
            self.__connection__.shutdown(py_socket.SHUT_RDWR)
            self.__connection__.close()
        except Exception as err:
            error = "Failed to stop Crawler's server! {}".format(err)
            LOGGER.error(error)
            return False
            
        self.__connection__ = None
        return True


if __name__ == '__main__':
    h = Host(DEFAULT_IP, DEFAULT_PORT)
    h.start_server()
    assert h.server_is_on, True
