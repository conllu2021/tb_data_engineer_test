'''Read an input parquet file from the NYC "Yellow Taxi" Trips Data and generate
an output parquet file from the input file selecting all the rows with trip distances 
(column trip_distance) greater than or equal to a given percentile.
'''
import argparse
import os
from argparse import ArgumentParser, Namespace
from typing import Final
import sys
import duckdb

MIN_PYTHON_VERSION: Final[tuple[int, int]] = (3, 8)
URL_PREFIX: Final[str] = 'https://'
SQL_FILE_PATH: Final[str] = './sql/query.sql'
DEFAULT_PERCENTILE: Final[int] = 90

def check_min_python_version() -> None:
    '''Check the minimun compatible version of Python.'''

    if sys.version_info < MIN_PYTHON_VERSION:
        sys.exit(f'Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]} or later is required.\n')

def check_path(input_file: str) -> str:
    '''Check if input_file is a correct path.'''

    if (
        (os.path.isfile(input_file) or input_file.startswith(URL_PREFIX))
        and (input_file.endswith('.parquet'))
    ):
        return input_file

    raise FileNotFoundError('input_file should be a path or a URL to a parquet file.\n')

def load_arguments() -> Namespace:
    '''Load all the arguments.'''

    parser: ArgumentParser = argparse.ArgumentParser(
        description='''Read an input parquet file from the NYC "Yellow Taxi" Trips Data and
        generate an output parquet file from the input file selecting all the rows with
        trip distances (column trip_distance) greater than or equal to a given percentile.
        ''',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        'input_file', 
        type=check_path,
        help='''path to a parquet file from the  NYC "Yellow Taxi" Trips Data.
        This can be either a local file ('path/to/file.parquet')
        or a URL ('https://path/to/file.parquet') ending with .parquet.
        ''',
    )
    parser.add_argument(
        '--percentile', 
        required=False,
        default=DEFAULT_PERCENTILE,
        type=int,
        choices=range(1,101),
        metavar='[1-100]',
        help='integer value of the Nth percentile.',
    )
    return parser.parse_args()

def generate_output(args: Namespace) -> None:
    '''Read the input file and generate an output file including only the rows greater than or 
    equal to the given percentile'''

    with open(SQL_FILE_PATH, 'r', encoding="utf-8") as file:
        query_templace: str = file.read()

    query: str = query_templace.format(
        input_file=args.input_file,
        percentile=args.percentile,
        output_file=f'output_{os.path.basename(args.input_file)}'
    )

    duckdb.query(query)

    print('Done!\n')


if __name__ == '__main__':
    check_min_python_version()
    generate_output(load_arguments())
