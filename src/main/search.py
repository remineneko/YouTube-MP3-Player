from yt_dlp import YoutubeDL
from src.main.media_metadata import MediaMetadata


class SearchVideos:
    _SITE_MAPPING = {
        "YouTube":'ytsearch',
        "Bilibili":'bilisearch'
    }

    def __init__(self, storage, chosen_site):
        self._storage = storage
        self._search_key = self._SITE_MAPPING[chosen_site]
        self._limit = 20 # TODO: Change to storage.user_search_limit some time soon.
                         # Would be nice if it is customized for different sites

    def search(self, query):
        ydl = YoutubeDL({'noplaylist': "True", "add-header": "Accept:\'/\'", 'force-ipv4': 'True'})
        search_res = ydl.extract_info(f"{self._search_key}{self._limit}:{query}", download=False)['entries']
        return [MediaMetadata(i) for i in search_res]