def export_MD(movies):
    """
    Create Markdown File
    """
    MD_FORMAT = """
## {index}. {title_KR} ({title_EN}, {year})

![poster]({img_URL})

### 영화 정보
장르: {genre}<br>
감독: {director}<br>
상영 시간: {duration}<br>
국가: {country}<br>

### 출연진
{actors}<br>

### 줄거리
{summary}
    """
    MD_converted = []
    for movie in movies:
        MD_converted.append(MD_FORMAT.format(
            index=movie['index'],
            title_KR=movie['title_KR'],
            title_EN=movie['title_EN'],
            year=movie['year'],
            img_URL=movie['img_URL'],
            genre=" / ".join(movie['genre']),
            country=" / ".join(movie['country']),
            duration=movie['duration'],
            director=movie['director'][0]['name_KR'],
            actors="<br>".join(
                map(lambda k: "{}: {}".format(k['name_KR'], k['role']),
                    movie['actors'])),
            summary=movie['summary']
        ))

    return "\n".join(MD_converted)
