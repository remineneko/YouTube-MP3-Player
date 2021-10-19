from yt_dlp import YoutubeDL
from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from typing import Dict


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
            storage.url = url
            storage.vid_info = self.obtained_data

    def _load_info(self):
        obtained_data : Dict = self.inst.extract_info(self._url, download = False)
        if self._url_type == 'video':
            return [MediaMetadata(obtained_data)]
        else:
            return [MediaMetadata(i) for i in obtained_data['entries']]


if __name__ == "__main__":
    norm_url = "https://youtu.be/ETGWiArNaO0"
    playlist_url = "https://www.youtube.com/watch?v=O6vqvlHwkxk&list=PLj3JxVDwUCBlJEZ33x5vSjCCEnJImg1js"
    ns = AppStorage()
    LoadURL(norm_url, ns)
    print(ns.vid_info[0].to_dict())
    LoadURL(playlist_url, ns)
