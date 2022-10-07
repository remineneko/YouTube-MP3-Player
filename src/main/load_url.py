import yt_dlp
from yt_dlp import YoutubeDL
from src.main.storage import AppStorage
from src.main.media_metadata import MediaMetadata
from typing import Dict
from copy import deepcopy
from src.main.exceptions import *


class LoadURL:
    def __init__(self, url, storage:AppStorage = None):
        self._url = url
        if "list" in self._url:
            self._url_type = "playlist"
        else:
            self._url_type = "video"
        self.inst = YoutubeDL(
            {
                'format': 'bestaudio',
                'ignoreerrors': 'only_download'
            }
        )
        self.obtained_data = self._load_info()
        if storage is not None:
            self.storage = storage
            self.storage.vid_info = deepcopy(self.obtained_data)

    def _load_info(self):
        try:
            obtained_data : Dict = self.inst.extract_info(self._url, download = False)
            if self._url_type == 'video':
                return [MediaMetadata(obtained_data)]
            else:
                return [MediaMetadata(i) for i in obtained_data['entries']]
        except yt_dlp.utils.DownloadError as e:
            raise LoadError(str(e))


if __name__ == "__main__":
    norm_url = "https://youtu.be/ETGWiArNaO0"
    norm_url1 = 'https://www.youtube.com/watch?v=9R80DUsixGg'
    n2 = "https://youtu.be/SQeVTw3gxco"
    n3 = "https://youtu.be/INbxTEerZSk"
    playlist_url = "https://youtube.com/playlist?list=PLJvIki1AHV3FC1TzVRdQX0mg_ed-5P9IC"
    ns = AppStorage()
    print(LoadURL(n3, ns).obtained_data)
    # LoadURL(playlist_url, ns)
