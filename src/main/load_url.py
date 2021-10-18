from yt_dlp import YoutubeDL
from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from typing import Dict


class LoadURL:
    def __init__(self, url, storage:AppStorage):
        self._url = url
        if "list" in self._url:
            self._url_type = "playlist"
        else:
            self._url_type = "video"
        storage.url = url
        self.inst = YoutubeDL()
        storage.vid_info = self._load_info()

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
    print(len(list(ns.vid_info[0].keys())))
    LoadURL(playlist_url, ns)
