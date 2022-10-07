from typing import List, Dict
import copy
from src.main.media_metadata import MediaMetadata
from src.main.config import *


class AppStorage:
    def __init__(self, config_path = os.path.join(DATA_FOLDER,'config.ini')):
        self._all_videos_info : List[MediaMetadata] = []
        self._config_path = config_path
        self.now_playing : List[MediaMetadata] = []
        self.temp_search_storage = []

    @property
    def vid_info(self) -> List[MediaMetadata]:
        return copy.deepcopy(self._all_videos_info)

    @vid_info.setter
    def vid_info(self, info_obtained: List[MediaMetadata]):
        self._all_videos_info = copy.deepcopy(info_obtained)

    def remove_entry(self, entry):
        self._all_videos_info.remove(entry)

    def add_entry(self, entry):
        if type(entry) == list:
            self._all_videos_info.extend([e for e in entry if e not in self._all_videos_info])
        else:
            if entry not in self.vid_info:
                self._all_videos_info.append(entry)

    def modify_pl_config(self, new_value):
        modify_pl_loc(self._config_path, new_value)

    def modify_music_config(self, new_value):
        modify_music_loc(self._config_path, new_value)

    def modify_flush_config(self, new_value):
        modify_flush_state(self._config_path, new_value)

    def get_user_music_path_choice(self):
        return get_user_music_location(self._config_path)

    def get_user_playlist_path_choice(self):
        return get_user_playlist_default_folder(self._config_path)

    def get_user_flush_choice(self):
        return get_user_flush_choice(self._config_path)

    def get_search_data(self, obj):
        self.temp_search_storage = copy.deepcopy(obj)

    def flush_temp_data(self):
        self.temp_search_storage.clear()