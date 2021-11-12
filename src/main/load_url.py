from yt_dlp import YoutubeDL
from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from typing import Dict
from copy import deepcopy


class LoadURL:
    def __init__(self, url, storage:AppStorage = None):
        self._url = url
        if "list" in self._url:
            self._url_type = "playlist"
        else:
            self._url_type = "video"
        self.inst = YoutubeDL()
        self.obtained_data = self._load_info()
        if storage is not None:
            self.storage = storage
            self.storage.url = url
            self.storage.vid_info = deepcopy(self.obtained_data)

    def _load_info(self):
        obtained_data : Dict = self.inst.extract_info(self._url, download = False)
        if self._url_type == 'video':
            return [MediaMetadata(obtained_data)]
        else:
            return [MediaMetadata(i) for i in obtained_data['entries']]


if __name__ == "__main__":
    norm_url = "https://youtu.be/ETGWiArNaO0"
    norm_url1 = 'https://www.youtube.com/watch?v=9R80DUsixGg'
    playlist_url = "https://www.youtube.com/watch?v=O6vqvlHwkxk&list=PLj3JxVDwUCBlJEZ33x5vSjCCEnJImg1js"
    ns = AppStorage()
    LoadURL(norm_url1, ns)
    print(ns.vid_info[0].chapters)
    # LoadURL(playlist_url, ns)
