from argparse import ArgumentParser

from crawler.utils.connection.client import Client


def main():
    ap = ArgumentParser()

    ap.add_argument("-i", "--ip_address",
                    type=str,
                    default=None,
                    required=True,
                    dest="ip_address",
                    help="Crawler's IP address",
                    metavar="IP_ADDRESS", action="store",
                    )

    ap.add_argument("-p", "--port",
                    type=str,
                    default=None,
                    required=True,
                    dest="port",
                    help="Crawler's connection port",
                    metavar="PORT", action="store",
                    )

    options = ap.parse_args()

    ip = options.ip_address
    port = options.port

    c = Client(host=ip, port=int(port))
    c.connect_to_host()

    while True:
        data = input("package: ")

        response = c.send_package_and_get_response(data)
        print(response)


if __name__ == '__main__':
    main()
