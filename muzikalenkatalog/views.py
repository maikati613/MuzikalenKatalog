import string
import unicodedata

from django.shortcuts import render
from django.utils.text import slugify

ALBUMS_PER_BLOCK = 9   # a moving artists strip appears after every 9 albums (3 rows of 3)

# TEMPORARY sample data (no database yet).
# Later the albums list is replaced by Album.objects.all().
SAMPLE_ALBUMS = [
    {"id": 1, "title": "Abbey Road", "artist": "The Beatles", "year": 1969,
     "description": "The last album the band recorded, known for its closing medley of short songs."},
    {"id": 2, "title": "Thriller", "artist": "Michael Jackson", "year": 1982,
     "description": "One of the best-selling albums ever, packed with pop and funk hits."},
    {"id": 3, "title": "The Dark Side of the Moon", "artist": "Pink Floyd", "year": 1973,
     "description": "A concept album about time, money and the mind."},
    {"id": 4, "title": "Back in Black", "artist": "AC/DC", "year": 1980,
     "description": "Heavy hard rock with huge riffs, made after a change of lead singer."},
    {"id": 5, "title": "Rumours", "artist": "Fleetwood Mac", "year": 1977,
     "description": "Smooth rock shaped by breakups happening inside the band."},
    {"id": 6, "title": "Nevermind", "artist": "Nirvana", "year": 1991,
     "description": "The album that brought grunge to a mass audience."},
    {"id": 7, "title": "OK Computer", "artist": "Radiohead", "year": 1997,
     "description": "Moody, atmospheric alternative rock about technology and isolation."},
    {"id": 8, "title": "Random Access Memories", "artist": "Daft Punk", "year": 2013,
     "description": "Electronic music with live musicians and a disco influence."},
    {"id": 9, "title": "Make It Big", "artist": "Wham!", "year": 1984,
     "description": "A bright pop album whose hits made the duo global stars."},
    {"id": 10, "title": "The Predator", "artist": "Ice Cube", "year": 1992,
     "description": "Hip-hop with sharp lyrics, released soon after the Los Angeles riots."},
    {"id": 11, "title": "It’s On (Dr. Dre) 187um Killa", "artist": "Eazy-E", "year": 1993,
     "description": "A West Coast rap EP famous for its feud with Dr. Dre."},
    {"id": 12, "title": "Arirang", "artist": "BTS", "year": 2026,
     "description": "BTS’s fifth studio album, their first group release in almost four years, named after a Korean folk song."},
    {"id": 13, "title": "Golden", "artist": "Jungkook", "year": 2023,
     "description": "The debut solo album of BTS member Jungkook, led by the hit “Seven”."},
    {"id": 14, "title": "In the Wee Small Hours", "artist": "Frank Sinatra", "year": 1955,
     "description": "A moody, late-night record often called one of the first concept albums."},
    {"id": 15, "title": "The Chronic", "artist": "Dr. Dre", "year": 1992,
     "description": "The solo debut that defined the smooth G-funk sound of West Coast hip-hop."},
    {"id": 16, "title": "Straight Outta Compton", "artist": "N.W.A", "year": 1988,
     "description": "A groundbreaking gangsta rap album that put West Coast hip-hop on the map."},
    {"id": 17, "title": "Kind of Blue", "artist": "Miles Davis", "year": 1959,
     "description": "A landmark modal jazz record, often named the best-selling jazz album."},
    {"id": 18, "title": "Purple Rain", "artist": "Prince", "year": 1984,
     "description": "The soundtrack album that mixed rock, funk and pop and made Prince a superstar."},
    {"id": 19, "title": "good kid, m.A.A.d city", "artist": "Kendrick Lamar", "year": 2012,
     "description": "A story-driven rap album about growing up in Compton."},
    {"id": 20, "title": "Hotel California", "artist": "Eagles", "year": 1976,
     "description": "Polished rock with a dark take on life in California."},
    {"id": 21, "title": "Led Zeppelin IV", "artist": "Led Zeppelin", "year": 1971,
     "description": "Hard rock and folk blended on an album that includes “Stairway to Heaven”."},
    {"id": 22, "title": "Appetite for Destruction", "artist": "Guns N’ Roses", "year": 1987,
     "description": "A raw, fast hard rock debut that became one of the best-selling debut albums."},
    {"id": 23, "title": "21", "artist": "Adele", "year": 2011,
     "description": "A soulful pop album about heartbreak, led by “Rolling in the Deep”."},
    {"id": 24, "title": "Future Nostalgia", "artist": "Dua Lipa", "year": 2020,
     "description": "Disco-influenced dance pop with a retro feel."},
    {"id": 25, "title": "Illmatic", "artist": "Nas", "year": 1994,
     "description": "Nas’s debut, a tight set of vivid New York street stories that became a hip-hop benchmark."},
    {"id": 26, "title": "Born to Run", "artist": "Bruce Springsteen", "year": 1975,
     "description": "A grand, cinematic rock album about escape and big dreams that broke Springsteen through."},
    {"id": 27, "title": "Blonde", "artist": "Frank Ocean", "year": 2016,
     "description": "An introspective, genre-bending R&B album about love, memory and growing up."},
    {"id": 28, "title": "Lemonade", "artist": "Beyoncé", "year": 2016,
     "description": "A visual album that moves from betrayal to healing, mixing pop, rock, country and R&B."},
    {"id": 29, "title": "Back to Black", "artist": "Amy Winehouse", "year": 2006,
     "description": "Retro soul with raw, confessional lyrics, led by “Rehab”."},
    {"id": 30, "title": "The Miseducation of Lauryn Hill", "artist": "Lauryn Hill", "year": 1998,
     "description": "A solo debut blending soul, R&B and hip-hop that won five Grammy Awards."},
    {"id": 31, "title": "Highway 61 Revisited", "artist": "Bob Dylan", "year": 1965,
     "description": "Dylan’s electric breakthrough, opening with “Like a Rolling Stone”."},
    {"id": 32, "title": "Songs in the Key of Life", "artist": "Stevie Wonder", "year": 1976,
     "description": "A sprawling double album of soul, funk and jazz that won Album of the Year."},
    {"id": 33, "title": "1989", "artist": "Taylor Swift", "year": 2014,
     "description": "Swift’s full move to pop, led by “Shake It Off”."},
    {"id": 35, "title": "Map of the Soul: 7", "artist": "BTS", "year": 2020,
     "description": "BTS’s fourth Korean studio album, led by “ON”."},
    {"id": 36, "title": "Currents", "artist": "Tame Impala", "year": 2015,
     "description": "Psychedelic synth-pop about change, led by “The Less I Know the Better”."},
    {"id": 37, "title": "Rebel Yell", "artist": "Billy Idol", "year": 1983,
     "description": "Billy Idol’s second solo album, mixing punk attitude with glossy 80s rock, led by the title track."},
    {"id": 38, "title": "Love Deluxe", "artist": "Sade", "year": 1992,
     "description": "Smooth, late-night soul and jazz-pop, led by “No Ordinary Love”."},
    {"id": 39, "title": "ASTROWORLD", "artist": "Travis Scott", "year": 2018,
     "description": "A psychedelic trap album led by “SICKO MODE”."},
    {"id": 40, "title": "AM", "artist": "Arctic Monkeys", "year": 2013,
     "description": "Heavy riffs meet R&B grooves, led by “Do I Wanna Know?”."},
    {"id": 41, "title": "Lethal Injection", "artist": "Ice Cube", "year": 1993,
     "description": "A G-funk-flavoured follow-up to The Predator, featuring “You Know How We Do It”."},
    {"id": 42, "title": "Doggystyle", "artist": "Snoop Dogg", "year": 1993,
     "description": "Snoop’s Dr. Dre-produced debut, a landmark of G-funk led by “Gin and Juice”."},
    {"id": 43, "title": "Blood on the Dance Floor", "artist": "Michael Jackson", "year": 1997,
     "description": "A remix album that mixes new songs with reworked tracks from HIStory."},
    {"id": 44, "title": "Bad", "artist": "Michael Jackson", "year": 1987,
     "description": "The follow-up to Thriller, which produced five US number-one singles."},
    {"id": 45, "title": "War & Peace Vol. 1 (The War Disc)", "artist": "Ice Cube", "year": 1998,
     "description": "An aggressive, hard-hitting set of West Coast rap."},
    {"id": 46, "title": "War & Peace Vol. 2 (The Peace Disc)", "artist": "Ice Cube", "year": 2000,
     "description": "The follow-up, with a more melodic, laid-back West Coast sound."},
]

# Artists shown in the moving strips.
# "slug" is the picture file name: static/artists/<slug>.jpg
SAMPLE_ARTISTS = [
    {"name": "Michael Jackson", "slug": "michael-jackson", "genre": "Pop", "song": "Billie Jean"},
    {"name": "Wham!", "slug": "wham", "genre": "Pop", "song": "Last Christmas"},
    {"name": "Ice Cube", "slug": "ice-cube", "genre": "Hip-Hop", "song": "It Was a Good Day"},
    {"name": "The Beatles", "slug": "the-beatles", "genre": "Rock", "song": "Hey Jude"},
    {"name": "Pink Floyd", "slug": "pink-floyd", "genre": "Progressive Rock", "song": "Wish You Were Here"},
    {"name": "Nirvana", "slug": "nirvana", "genre": "Grunge", "song": "Smells Like Teen Spirit"},
    {"name": "Radiohead", "slug": "radiohead", "genre": "Alternative Rock", "song": "Creep"},
    {"name": "Daft Punk", "slug": "daft-punk", "genre": "Electronic", "song": "One More Time"},
    {"name": "Fleetwood Mac", "slug": "fleetwood-mac", "genre": "Rock", "song": "Dreams"},
    {"name": "AC/DC", "slug": "ac-dc", "genre": "Hard Rock", "song": "Highway to Hell"},
    {"name": "Dr. Dre", "slug": "dr-dre", "genre": "Hip-Hop", "song": "Still D.R.E."},
    {"name": "Eazy-E", "slug": "eazy-e", "genre": "Hip-Hop", "song": "Boyz-n-the-Hood"},
    {"name": "BTS", "slug": "bts", "genre": "K-pop", "song": "Dynamite"},
    {"name": "Jungkook", "slug": "jungkook", "genre": "K-pop", "song": "Seven"},
    {"name": "Frank Sinatra", "slug": "frank-sinatra", "genre": "Vocal Jazz", "song": "My Way"},
    {"name": "N.W.A", "slug": "nwa", "genre": "Hip-Hop", "song": "Straight Outta Compton"},
    {"name": "Miles Davis", "slug": "miles-davis", "genre": "Jazz", "song": "So What"},
    {"name": "Prince", "slug": "prince", "genre": "Pop / Funk", "song": "Purple Rain"},
    {"name": "Kendrick Lamar", "slug": "kendrick-lamar", "genre": "Hip-Hop", "song": "HUMBLE."},
    {"name": "Eagles", "slug": "eagles", "genre": "Rock", "song": "Hotel California"},
    {"name": "Led Zeppelin", "slug": "led-zeppelin", "genre": "Hard Rock", "song": "Stairway to Heaven"},
    {"name": "Guns N’ Roses", "slug": "guns-n-roses", "genre": "Hard Rock", "song": "Sweet Child o’ Mine"},
    {"name": "Adele", "slug": "adele", "genre": "Pop", "song": "Rolling in the Deep"},
    {"name": "Dua Lipa", "slug": "dua-lipa", "genre": "Pop", "song": "Levitating"},
]


def _norm(text):
    """lower-case, no accents, no spaces or punctuation: "N.W.A" -> "nwa", "Beyoncé" -> "beyonce" """
    text = unicodedata.normalize("NFKD", text).casefold().replace("&", "and")
    return "".join(ch for ch in text if ch.isalnum())


def home(request):
    q = request.GET.get("q", "").strip()

    albums = SAMPLE_ALBUMS
    nq = _norm(q)
    if nq:   # search by album title OR artist name
        albums = [a for a in albums if nq in _norm(a["title"]) or nq in _norm(a["artist"])]

    # alphabetical order, so the A-Z bar can jump to the first album of a letter
    albums = sorted(albums, key=lambda a: a["title"].casefold())

    seen = set()
    cards = []
    for a in albums:
        letter = a["title"][0].upper()
        cards.append(dict(a, hue=(a["id"] * 47) % 360, letter=letter,
                          slug=slugify(a["title"]),
                          first_of_letter=letter not in seen))
        seen.add(letter)

    letters = [{"char": c, "has": c in seen} for c in string.ascii_uppercase]

    artists = []
    for i, a in enumerate(SAMPLE_ARTISTS):
        initials = "".join(w[0] for w in a["name"].split()[:2]).upper()
        artists.append(dict(a, hue=(i * 47 + 20) % 360, initials=initials))

    # split the albums into blocks; after every full block comes a moving artists strip
    blocks = []
    for start in range(0, len(cards), ALBUMS_PER_BLOCK):
        part = cards[start:start + ALBUMS_PER_BLOCK]
        strip = None
        if len(part) == ALBUMS_PER_BLOCK:
            shift = (len(blocks) * 8) % len(artists)   # each strip starts with different artists
            strip = artists[shift:] + artists[:shift]
        blocks.append({"albums": part, "artists": strip})

    return render(request, "index.html", {
        "albums": cards, "blocks": blocks, "q": q, "letters": letters,
    })
