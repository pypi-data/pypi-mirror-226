from argparse import ArgumentParser, Namespace
from os import environ
from pathlib import Path
from sys import exit

from rich.logging import RichHandler

from trongrid_extractoor.config import log
from trongrid_extractoor.helpers.address_helpers import address_of_symbol, is_contract_address, print_symbol_addresses
from trongrid_extractoor.helpers.time_helpers import str_to_timestamp
from trongrid_extractoor.helpers.string_constants import TRANSFER


parser = ArgumentParser(
    description='Pull transactions for a given token. Either --token or --resume-csv must be provided. ',
    epilog='For a limited number of known symbols (USDT, USDD, etc.) you can use the symbol string instead ' \
           'of the on chain address.'
)

parser.add_argument('-t', '--token',
                    help="Token address or a symbol string like 'USDT'",
                    metavar='TOKEN_ADDRESS_OR_SYMBOL')

parser.add_argument('-e', '--event-name',
                    help="name of the event to extract ('None' to get all events)",
                    metavar='EVENT_NAME',
                    default=TRANSFER)

parser.add_argument('-s', '--since',
                    help='extract transactions up to and including this time (ISO 8601 Format)',
                    metavar='DATETIME')

parser.add_argument('-u', '--until',
                    help='extract transactions starting from this time (ISO 8601 Format)',
                    metavar='DATETIME')

# TODO: this should accept an S3 URI.
parser.add_argument('-o', '--output-dir',
                    help='write transaction CSVs to a file in this directory',
                    metavar='OUTPUT_DIR')

parser.add_argument('-r', '--resume-from-csv',
                    help='resume extracting to a partially extracted CSV file',
                    metavar='CSV_FILE')

parser.add_argument('-l', '--list-symbols', action='store_true',
                    help='print a list of known symbols that can be used with the --token argument and exit')

parser.add_argument('-d', '--debug', action='store_true',
                    help='set LOG_LEVEL to DEBUG (can also be set with the LOG_LEVEL environment variable)')


def parse_args() -> Namespace:
    args = parser.parse_args()
    setup_logging(args)
    args.output_dir = Path(args.output_dir or '')
    args.resume_from_csv = Path(args.resume_from_csv) if args.resume_from_csv else None

    if args.list_symbols:
        print_symbol_addresses()
        exit()

    if args.token and not is_contract_address(args.token):
        address = address_of_symbol(args.token)

        if address is None:
            log.error(f"Unknown symbol: '{args.token}'")
            exit(1)
        else:
            log.info(f"Using '{args.token}' address '{address}'")
            args.token = address

    if args.since:
        since = str_to_timestamp(args.since)
        log.info(f"Requested records since '{args.since}' which parsed to {since}.")
        args.since = since

    if args.until:
        until = str_to_timestamp(args.until)
        log.info(f"Requested records until '{args.until}' which parsed to {until}.")
        args.until = until

    if args.event_name == 'None':
        args.event_name = None

    log.debug(f"Processed arguments: {args}")
    return args


def setup_logging(args: Namespace) -> None:
    log_level = 'DEBUG' if args.debug else environ.get('LOG_LEVEL', 'INFO')
    log.setLevel(log_level)
    rich_stream_handler = RichHandler(rich_tracebacks=True)
    rich_stream_handler.setLevel(log_level)

    log.addHandler(rich_stream_handler)
