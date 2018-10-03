from urllib.request import urlopen, Request, unquote
from bs4 import BeautifulSoup as Soup
from pprint import pprint


def parse_URL(URL):
    req = Request(
        URL,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    html = Soup(urlopen(req).read().decode('utf-8'), 'html.parser')
    return html


def parse_movie(code):
    html = parse_URL("https://movie.daum.net/moviedb/main?movieId={}"
                     .format(code))
    info = html.find('div', {'class': 'movie_summary'})

    movie = {
        'title_KR': None,
        'title_EN': None,
        'country': [],
        'genre': [],
        'duration': None,
        'rating': None,
        'img_URL': None,  # Small Image
    }
    movie['title_KR'] = info.find('strong',
                                  {'class': 'tit_movie'}).text.strip()
    movie['title_EN'] = info.find('span',
                                  {'class': 'txt_origin'}).text.strip()

    movie['genre'] = info.find('dd',
                               {'class': 'txt_main'}).text.split('/')

    movie['country'] = list(map(str.strip, info.find('dl',
                                                     {'class': 'list_movie'})
                                .find_all('dd')[1].text.split(',')))

    movie['duration'], movie['rating'] = list(map(str.strip, info.find(
        'dl', {'class': 'list_movie'}).find_all('dd')[-3].text.split(',')))

    movie['img_URL'] = unquote(html.find('img')['src'].split('fname=')[1])

    return movie


def main():
    movie = parse_movie(code=3236)
    pprint(movie)


if __name__ == "__main__":
    main()
