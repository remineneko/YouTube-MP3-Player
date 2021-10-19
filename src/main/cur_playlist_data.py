from typing import List
from src.main.media_metadata import MediaMetadata
from src.main.load_url import LoadURL
import os
import json


class Playlist:
    def __init__(self, data: List[MediaMetadata]):
        self._data = [f.to_simple_dict() for f in data]

    def save(self, file_name, file_loc):
        with open(os.path.join(file_loc, '{}.json'.format(file_name)), 'w') as f:
            json.dump(self._data, f)

    def load(self, file_name, file_loc):
        with open(os.path.join(file_loc, '{}.json'.format(file_name)), 'r') as f:
            base_data = json.load(f)
            result = [LoadURL(i['url']).obtained_data[0] for i in base_data]
            return result


if __name__ == "__main__":
    from settings import *

    mock_url = "https://youtu.be/ETGWiArNaO0"

    song_info = LoadURL(mock_url).obtained_data
    try:
        os.mkdir(DEFAULT_PLAYLISTS_FOLDER, mode = 0o777)
    except FileExistsError:
        pass
    Playlist(song_info).save("test_1",DEFAULT_PLAYLISTS_FOLDER)
    data = Playlist(song_info).load("test_1", DEFAULT_PLAYLISTS_FOLDER)
    print(data)

