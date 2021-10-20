from typing import List, Dict
import copy
from src.main.media_metadata import MediaMetadata


class AppStorage:
    def __init__(self):
        self._given_url = None
        self._all_videos_info : List[MediaMetadata] = []
        self.config = self.load_config()
        self.now_playing : List[MediaMetadata] = []

    @property
    def url(self) -> str:
        return self._given_url

    @url.setter
    def url(self, new_url:str):
        self._given_url = new_url

    @property
    def vid_info(self) -> List[MediaMetadata]:
        return copy.deepcopy(self._all_videos_info)

    @vid_info.setter
    def vid_info(self, info_obtained: List[Dict]):
        self._all_videos_info = copy.deepcopy(info_obtained)

    def load_config(self):
        '''
        Loads the config for the program.
        :return:
        '''
        return None

    def remove_entry(self, entry):
        self._all_videos_info.remove(entry)

    def add_entry(self, entry):
        if type(entry) == list:
            self._all_videos_info.extend(entry)
        else:
            if entry not in self.vid_info:
                self._all_videos_info.append(entry)