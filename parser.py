from urllib.request import urlopen, Request, unquote, quote
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup as Soup
from error import raise_error


def parse_URL(URL):
    """
    Descrpition:
        This function send request for HTML data with user-agent.

    Returns:
        <Soup> class data (BeautifulSoup class)
    """

    req = Request(
        URL,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' +
            'Chrome/35.0.1916.47 Safari/537.36'
        }
    )

    try:
        html = Soup(urlopen(req).read().decode('utf-8'), 'html.parser')
        return html

    except HTTPError:
        raise_error('Cannot parse HTML data.'
                    'Perhaps your movieID is incorrect?')
    except URLError:
        raise_error('Cannot parse data from the Internet.'
                    'Please check your network status.')


def parse_movie(code):
    """
    Description:
        This function fabricates and organizes movie data that was parsed from
        `https://movie.daum.net`.

    Returns:
        <dict type format data with following keys>

        'title_KR'  | Movie title in Korean                     | <str>
        'title_EN'  | Movie title in English                    | <str>
        'country'   | List of countries                         | <list>
        'genre'     | List of genres                            | <list>
        'year'      | Year of the movie release date            | <list>
        'duration'  | Total time of the movie                   | <str>
        'rating'    | Rating (age limit for audience)           | <str>
        'img_URL'   | URL of poster image file                  | <str>
        'summary'   | Short summary of movie                    | <str>
        'director'  | List of the director(s)                   | <list>
        'actors'    | List of actors                            | <list>

    Note:
        For 'director' and 'actors', they consist of tuples with following
        format:

        'name_KR'   | Korean name of the person.                | <str>
        'name_EN'   | English name of the person (can be empty) | <str>
        'role'      | Person's role in the movie                | <str>

    """
    html = parse_URL("https://movie.daum.net/moviedb/main?movieId={}"
                     .format(code))
    info = html.find('div', {'class': 'movie_summary'})

    # Movie format
    movie = {
        'title_KR': None,
        'title_EN': None,
        'country': [],
        'genre': [],
        'year': None,
        'duration': None,
        'rating': None,
        'img_URL': None,
        'summary': None,
        'director': [],
        'actors': []
    }

    try:
        # Parse each keys from the html data
        title = info.find(
            'strong', {'class': 'tit_movie'}).text.strip().split()
        movie['year'] = title.pop(-1)[1:-1]
        movie['title_KR'] = " ".join(title)
        movie['title_EN'] = info.find('span',
                                      {'class': 'txt_origin'}).text.strip()

        movie['genre'] = info.find('dd',
                                   {'class': 'txt_main'}).text.split('/')

        movie['country'] = list(
            map(str.strip, info.find('dl', {'class': 'list_movie'})
                .find_all('dd')[1].text.split(',')))

        movie['duration'], movie['rating'] = list(map(str.strip, info.find(
            'dl', {'class': 'list_movie'}).find_all('dd')[-3].text.split(',')))

        movie['img_URL'] = unquote(html.find('img')['src'].split('fname=')[1])

        movie['summary'] = html.find('div', {'class': 'desc_movie'})\
            .find('p').text.replace('\t', '').strip()

        # Parse director and actors info
        actors = html.find('ul', {'class': 'list_staff'})
        for li in actors.find_all('li'):
            staff = {}
            staff['name_KR'] = li.find('strong').find('em').text
            staff['name_EN'] = li.find('strong').text. \
                replace(staff['name_KR'], '').strip()
            staff['role'] = li.find(
                'span', {'class': 'txt_awards'}).text.strip()

            if staff['role'] == '감독':
                movie['director'].append(staff)
            else:
                movie['actors'].append(staff)

        return movie

    # Exception for any exception, raise error and halt
    except Exception:
        raise_error('Unable to parse data for movieId={} due to its unique'
                    'HTML settings.'.format(code))
