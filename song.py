class Song:
    """"Class to represent a song

    Attributtes:
        title (str): the title of the song
        artist (Artist): An artist object representing the song
        duration (int): The duration of the song in seconds. May by zero.
      """

    def __init__(self, title, artist, duration=0):

        self.title = title
        self.artist = artist
        self.duration = duration


class Album:
    """"Class repsresent an Album, using it's track list
    
    Attributes:
        name(str): The name of album
        year(int): The year was album was realased
        artist(Artist) The artist responsible for the album. If not specified,
        the artist will default to an artist with name 'Various Artist'
        tracks (List[Song]): A list of the songs on the album.

    Methods:
        add_song: Used to add new song to the album's track list
    """

    def __init__(self, name, year, artist=None):
        self.name = name
        self.year = year
        if artist is None:
            self.artist = Artist("Various Artist")
        else:
            self.artist = artist
        self.tracks = []

    def add_song(self, song, position=None):
        """ Adds a song to the track list

        Args:
            song(Song): a song to add.
            position(Optiona[int]): if specified, the song will be added to that positon
            in the track list - inserting it between other song if necessery.
            Otherwise, the song will be added to the end of the list.
        """
        if position is None:
            self.tracks.append(song)
        else:
            self.tracks.insert(position, song)


class Artist:
    """Basic class to store artist details.

    Atrributes:
    name(str): The name of the artist
    albums(list Album): List of the albums by this artist.
        The list includes only those albums in this collection,
        it is not an exhaustive list of the artist's published albums.

    Method:
    new_album: Use to add a new album to the artist's album list.
    """
    def __init__(self, name):
        self.name = name
        self.albums = []

    def add_album(self, album):
        """Add a new album to the albums list

        Args:
            ""album(Album): Album object to add to the new list.
            If th album is already present, it will not be added again (although is yet to implemented).
        """
        self.albums.append(album)


def find_object(field, object_list):
    """Check the "object_list" to see if the object "name" atributte equal to "field" exists, return it if so. """
    for item in object_list:
        if item.name == field:
            return item
    return None

def load_data():
    new_artist = None
    new_album = None
    artist_list = []
    with open("Udemy_Course/Object_Oriented_Programing_and_Classes/OOP_Song_Class/albums.txt", "r") as albums_file:
        for line in albums_file:
            # data row should consist of (artist, album, year, song)
            artist_filed, album_field, year_field, song_field = tuple(line.strip("\n").split("\t"))
            year_field = int(year_field)

            if new_artist is None:
                new_artist = Artist(artist_filed)
                artist_list.append(new_artist)
            elif new_artist.name != artist_filed:
                # We'have just read deatils for new_artist
                # retrieve the artist object if there is one,
                # otherwise create a new object and add it to the artist list
                new_artist = find_object(artist_filed, artist_list)
                if new_artist is None:
                    new_artist = Artist(artist_filed)
                    artist_list.append(new_artist)
                new_album = None

            if new_album is None:
                new_album = Album(album_field, year_field, new_artist)
                new_artist.add_album(new_album)
            elif new_album.name != album_field:
                # We'have just read a new album for the current artist
                # retrieve the album object if there is one,
                # otherwise create a new album object and store it in the artist's collection
                new_album = find_object(album_field, new_artist.albums)
                if new_album is None:
                    new_album = Album(album_field, year_field, new_artist)
                    new_artist.add_album(new_album)

            # create new song object end add it to current album's collection
            new_song = Song(song_field, new_artist)
            new_album.add_song(new_song)
    return artist_list


def create_chceckfile(artist_list):
    """Create a check file from the object data for compairson with the original file"""
    with open("Udemy_Course/Object_Oriented_Programing_and_Classes/OOP_Song_Class/checkfile.txt", "w") as checkfile:
        for new_artist in artist_list:
            for new_album in new_artist.albums:
                for new_song in new_album.tracks:
                    print("{0.name}\t{1.name}\t{1.year}\t{2.title}".format
                          (new_artist, new_album, new_song), file=checkfile)


if __name__ == "__main__":
    artists = load_data()
    print(artists)
    print("There are {} artist". format(len(artists)))
    create_chceckfile(artists)
