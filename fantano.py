"""Stores Fantano class."""
import spotipy
import re

from scores import titles_classics
from scores import titles_2010s
from scores import titles_manual
from scores_2020s import titles_2020s


class Fantano:
    """Stores all user data for the home page."""
    total_albums = 0
    eligible_albums = []
    scored_albums = {}
    classic_albums = {
        # 2000s
        "Daft Punk - Discovery",
        "System Of A Down - Toxicity",
        "Björk - Vespertine",
        "Godspeed You! Black Emperor - Lift Your Skinny Fists Like Antennas to Heaven",
        "Madvillain & Madlib & MF DOOM - Madvillainy",
        # 190s
        "Ms. Lauryn Hill - The Miseducation of Lauryn Hill",
        "Nirvana - Nevermind",
        "Nirvana - Nevermind (Deluxe Edition)",
        "Nirvana - Nevermind (Remastered)",
        "Nirvana - Nevermind (Super Deluxe Edition)",
        "Nirvana - Nevermind (30th Anniversary Super Deluxe)",
        "Neutral Milk Hotel - In the Aeroplane Over the Sea",
        "Wu-Tang Clan - Enter The Wu-Tang (36 Chambers)",
        "Wu-Tang Clan - Enter The Wu-Tang (36 Chambers) [Expanded Edition]",
        "Depeche Mode - Violator (2006 Remaster)",
        # 1980s
        "Metallica - Master of Puppets (Remastered)",
        "Metallica - Master of Puppets (Remastered Deluxe Box Set)",
        "Public Enemy - It Takes A Nation Of Millions To Hold Us Back",
        "Public Enemy - It Takes A Nation Of Millions To Hold Us Back (Deluxe Edition)",
        "Kate Bush - Hounds of Love (2018 Remaster)",
        "Talking Heads - Remain in Light",
        "Talking Heads - Remain in Light (Deluxe Version)",
        "Prince - Purple Rain",
        "Prince - Purple Rain (Deluxe Expanded Edition)",
        # 1970s
        "Miles Davis - Bitches Brew",
        "Miles Davis - Bitches Brew (Legacy Edition)",
        "The Clash - London Calling (Remastered)",
        "The Clash - London Calling (Expanded Edition)",
        "Marvin Gaye - What's Going On",
        "Marvin Gaye - What's Going On (Deluxe Edition/50th Anniversary)",
        "Led Zeppelin - Physical Graffiti (Remaster)",
        "Led Zeppelin - Physical Graffiti (Deluxe Edition)",
        "Television - Marquee Moon",
        # 1960s
        "Frank Zappa - Hot Rats",
        "Bob Dylan - Highway 61 Revisited",
        "Charles Mingus - The Black Saint And The Sinner Lady",
        "The Beatles - Abbey Road (Remastered)",
        "The Beatles - Abbey Road (Super Deluxe Edition)",
        "Nina Simone - Nina Simone Sings The Blues (Expanded Edition)",
    }
    flairs = [
        " (remaster)",
        " (remastered)",
        " (deluxe)",
        " (deluxe edition)",
        " (deluxe expanded edition)",
        " (deluxe version)",
        " (extended)",
        " (extended edition)",
        " (expanded edition)",
        " [expanded edition]",
        " (special version)",
        " (special edition)",
        " (super deluxe)",
        " (super deluxe edition)",
        " (bonus track version)",
        " [platinum edition]",
        " (edición especial)",
        # specific to particular albums
        " (the platinum pleasure edition)",  # Jessie Ware- What's Your Pleasure?
        " (30th anniversary super deluxe)",  # Nirvana - Nevermind
        " (2006 remaster)",  # Depeche Mode - Violator
        " (remastered deluxe box set)",  # Metallica - Master of Puppets
        " (2018 remaster)",  # Kate Bush - Hounds of Love
        " (mirror to mirror)",  # Car Seat Headrest - Twin Fantasy
        " (original)",  # The Weeknd - House Of Balloons
        " (legacy edition)",  # Miles Davis - Bitches Brew
        " (deluxe edition/50th anniversary)",  # Marvin Gaye - What's Going On
    ]

    def __init__(self, token):
        """Authorize through Spotify."""
        self.sp = spotipy.Spotify(auth=token)

    def get_eligible_albums(self):
        """Retrieve all albums saved by the user that potentially have a score."""
        self.eligible_albums = []
        saved_albums = self.sp.current_user_saved_albums(limit=50, offset=0)['items']
        total = 10000  # spotify limit?

        # compile every album saved by user into list
        offset = int(50)
        while offset < (total + 50):
            saved_albums.extend(self.sp.current_user_saved_albums(limit=50, offset=offset)['items'])
            offset = offset + 50
            if len(saved_albums) < offset:
                break

        # get total number of albums in library
        self.total_albums = len(saved_albums)

        for i in saved_albums:
            release_year = int((i['album']['release_date'])[0:4])
            title = i['album']['name']
            artist = ' & '.join(artist['name'] for artist in i['album']['artists'])
            score = -1
            link = i['album']['external_urls']['spotify']

            if (release_year >= 2010) and (i['album']['album_type'] == 'album'):
                # potentially has Fantano score
                self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
            elif (artist + ' - ' + title in self.classic_albums):
                # is a scored classic album
                self.eligible_albums.append(list((artist + ' - ' + title, score, link)))
        return

    def get_user_scores(self):
        """Assign scores to saved albums."""
        self.scored_albums = {}
        for i in self.eligible_albums:

            search = self.remove_extras(i[0].lower())
            search_group_first = ' '
            search_group_last = ' '
            if ' & ' in search:
                search_group_last = search.split(' & ')[-1].split(' - ')[0] + ' - ' + search.split(' - ', 1)[1]
                search_group_first = search.split(' & ')[0] + ' - ' + search.split(' - ', 1)[1]

            all_titles = {**titles_classics, **titles_2010s, **titles_2020s, **titles_manual}

            if search in all_titles:
                self.scored_albums[self.remove_extras(i[0])] = (all_titles[search], i[2])
                i[1] = all_titles[search]
            elif search_group_first in all_titles:
                self.scored_albums[self.remove_extras(i[0])] = (all_titles[search_group_first], i[2])
                i[1] = all_titles[search_group_first]
            elif search_group_last in all_titles:
                self.scored_albums[self.remove_extras(i[0])] = (all_titles[search_group_last], i[2])
                i[1] = all_titles[search_group_last]
        return

    def remove_extras(self, album):
        for flair in self.flairs:
            remove_flair = re.compile(re.escape(flair), re.IGNORECASE)
            album = remove_flair.sub('', album)
        return album
