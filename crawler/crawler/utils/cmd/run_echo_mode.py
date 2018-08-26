from argparse import ArgumentParser

from crawler.core import Crawler


def main():
    ap = ArgumentParser()

    ap.add_argument("-i", "--ip_address",
                    type=str,
                    default=None,
                    required=False,
                    dest="ip_address",
                    help="Crawler's IP address",
                    metavar="IP_ADDRESS", action="store",
                    )

    ap.add_argument("-p", "--port",
                    type=str,
                    default=None,
                    required=False,
                    dest="port",
                    help="Crawler's connection port",
                    metavar="PORT", action="store",
                    )

    options = ap.parse_args()

    ip = options.ip_address
    try:
        port = int(options.port)
    except:
        port = None

    c = Crawler(ip=ip, port=port)
    c.echo()


if __name__ == '__main__':
    main()
