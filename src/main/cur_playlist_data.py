from typing import List
from src.main.media_metadata import MediaMetadata
from src.main.load_url import LoadURL
from src.main.exceptions import *
import json


class Playlist:
    def __init__(self, data: List[MediaMetadata] = None):
        if data is not None:
            self._data = [f.to_simple_dict() for f in data]

    def save(self, file_loc):
        with open(file_loc, 'w') as f:
            json.dump(self._data, f)

    @staticmethod
    def load(file_loc:str):
        with open(file_loc, 'r') as f:
            if file_loc.split(".")[1].lower() == 'json':
                base_data = json.load(f)
                try:
                    result = [LoadURL(i['url']).obtained_data[0] for i in base_data]
                    return result
                except LoadError as e:
                    raise LoadError(str(e))
                except Exception:
                    raise IncorrectJSONFileError("This is not the correctly outputted json file")
            else:
                raise IncorrectFileTypeError("Given file must be a JSON file")


