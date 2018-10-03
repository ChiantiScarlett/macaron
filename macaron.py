from pprint import pprint
from json import loads
from re import sub
from parser import parse_movie

FILENAME = 'example.json'
OUTPUT = 'example.md'


def main():
    with open(FILENAME, encoding='utf-8') as fp:
        data = sub('[\n\t]', '', fp.read().replace('    ', ''))
        data = loads(data)

    # sort data by index
    data = sorted(data, key=lambda k: k['index'])
    for movie in data:
        movie = parse_movie(code=movie['movieId'])
        pprint(movie)
