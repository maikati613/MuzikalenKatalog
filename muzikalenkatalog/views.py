import string

from django.shortcuts import render

# TEMPORARY sample data (no database yet).
# Later the albums list is replaced by Album.objects.all().
SAMPLE_ALBUMS = [
    {"id": 1, "title": "Abbey Road", "artist": "The Beatles", "year": 1969,
     "description": "Последният записан албум на групата, с известната странична страна от преплетени песни."},
    {"id": 2, "title": "Thriller", "artist": "Michael Jackson", "year": 1982,
     "description": "Един от най-продаваните албуми в историята, пълен с поп и фънк хитове."},
    {"id": 3, "title": "The Dark Side of the Moon", "artist": "Pink Floyd", "year": 1973,
     "description": "Концептуален прогресив рок албум за времето, парите и ума."},
    {"id": 4, "title": "Back in Black", "artist": "AC/DC", "year": 1980,
     "description": "Тежък хард рок с огромни рифове, записан след смяна на вокалиста."},
    {"id": 5, "title": "Rumours", "artist": "Fleetwood Mac", "year": 1977,
     "description": "Меко звучене и истории за раздели, създадени по време на лични кризи в групата."},
    {"id": 6, "title": "Nevermind", "artist": "Nirvana", "year": 1991,
     "description": "Албумът, който изведе гръндж звученето до масовата публика."},
    {"id": 7, "title": "OK Computer", "artist": "Radiohead", "year": 1997,
     "description": "Мрачен и атмосферен алтернативен рок за технологиите и отчуждението."},
    {"id": 8, "title": "Random Access Memories", "artist": "Daft Punk", "year": 2013,
     "description": "Електронна музика със жив оркестър и вдъхновение от диското."},
    {"id": 9, "title": "Make It Big", "artist": "Wham!", "year": 1984,
     "description": "Ярък поп албум с хитове, които направиха дуото световно известно."},
    {"id": 10, "title": "The Predator", "artist": "Ice Cube", "year": 1992,
     "description": "Хип-хоп албум с остри текстове, издаден малко след размириците в Лос Анджелис."},
]

# Artists shown in the moving strip at the bottom of the page.
# "slug" is the picture file name: static/artists/<slug>.jpg
SAMPLE_ARTISTS = [
    {"name": "Michael Jackson", "slug": "michael-jackson", "genre": "Поп", "song": "Billie Jean"},
    {"name": "Wham!", "slug": "wham", "genre": "Поп", "song": "Last Christmas"},
    {"name": "Ice Cube", "slug": "ice-cube", "genre": "Хип-хоп", "song": "It Was a Good Day"},
    {"name": "The Beatles", "slug": "the-beatles", "genre": "Рок", "song": "Hey Jude"},
    {"name": "Pink Floyd", "slug": "pink-floyd", "genre": "Прогресив рок", "song": "Wish You Were Here"},
    {"name": "Nirvana", "slug": "nirvana", "genre": "Гръндж", "song": "Smells Like Teen Spirit"},
    {"name": "Radiohead", "slug": "radiohead", "genre": "Алтернативен рок", "song": "Creep"},
    {"name": "Daft Punk", "slug": "daft-punk", "genre": "Електронна", "song": "One More Time"},
    {"name": "Fleetwood Mac", "slug": "fleetwood-mac", "genre": "Рок", "song": "Dreams"},
    {"name": "AC/DC", "slug": "ac-dc", "genre": "Хард рок", "song": "Back in Black"},
]


def home(request):
    q = request.GET.get("q", "").strip()

    albums = SAMPLE_ALBUMS
    if q:
        albums = [a for a in albums if q.casefold() in a["title"].casefold()]

    # alphabetical order, so the A-Z bar can jump to the first album of a letter
    albums = sorted(albums, key=lambda a: a["title"].casefold())

    seen = set()
    cards = []
    for a in albums:
        letter = a["title"][0].upper()
        cards.append(dict(a, hue=(a["id"] * 47) % 360, letter=letter,
                          first_of_letter=letter not in seen))
        seen.add(letter)

    letters = [{"char": c, "has": c in seen} for c in string.ascii_uppercase]

    artists = []
    for i, a in enumerate(SAMPLE_ARTISTS):
        initials = "".join(w[0] for w in a["name"].split()[:2]).upper()
        artists.append(dict(a, hue=(i * 47 + 20) % 360, initials=initials))

    return render(request, "index.html", {
        "albums": cards, "q": q, "letters": letters, "artists": artists,
    })
