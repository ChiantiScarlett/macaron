from pprint import pprint
from json import loads
from re import sub
from parser import parse_movie
from error import raise_error
import argparse


def main(args):
    # check if the file is in json format
    if not args.filename.lower().endswith(".json"):
        raise_error('This program can only read *.json file. '
                    'Refer to `example.json` for more details.')

    # Read json file
    try:
        with open(args.filename, encoding='utf-8') as fp:
            data = fp.read()
    except Exception:
        raise_error('Cannot find file `{}`.'.format(args.filename))

    # Check if the json file is in right format
    try:
        data = sub('[\n\t]', '', data.replace('    ', ''))
        data = loads(data)
    except Exception:
        raise_error('The JSON file is not in its format. Please take a look'
                    'at `example.json` and change the format accordingly.')

    # Sort data by index
    data = sorted(data, key=lambda k: k['index'])

    # Parse movie data
    for movie in data:
        movie = parse_movie(code=movie['movieId'])
        pprint(movie)


def read_args():
    # Set argument parser and read arguments
    parser = argparse.ArgumentParser()

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument('-f', dest='filename',
                               help='JSON FILE LOCATION', required=True)

    parser.add_argument('-o', dest='output',
                        help='OUTPUT FILENAME')

    args = parser.parse_args()

    # If output argument is None, set default value to FILENAME.md
    if args.output is None:
        args.output = ".".join(args.filename.split(".")[:-1]) + ".md"

    return args


if __name__ == "__main__":
    # Argument Parser

    args = read_args()
    main(args)
