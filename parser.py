from urllib.request import urlopen, Request, unquote
from bs4 import BeautifulSoup as Soup


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
        'year': None,
        'duration': None,
        'rating': None,
        'img_URL': None,
        'summary': None,
        'director': [],
        'actors': []
    }

    title = info.find('strong', {'class': 'tit_movie'}).text.strip().split()
    movie['year'] = title.pop(-1)[1:-1]
    movie['title_KR'] = " ".join(title)
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

    movie['summary'] = html.find('div', {'class': 'desc_movie'}).find('p') \
        .text.replace('\t', '').strip()

    # Parse director and actors info
    actors = html.find('ul', {'class': 'list_staff'})
    for li in actors.find_all('li'):
        staff = {}
        staff['name_KR'] = li.find('strong').find('em').text
        staff['name_EN'] = li.find('strong').text. \
            replace(staff['name_KR'], '').strip()
        staff['role'] = li.find('span', {'class': 'txt_awards'}).text.strip()

        if staff['role'] == '감독':
            movie['director'].append(staff)
        else:
            movie['actors'].append(staff)

    return movie