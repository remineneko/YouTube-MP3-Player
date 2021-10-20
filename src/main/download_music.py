from yt_dlp import YoutubeDL
from typing import List
from settings import *
from src.main.alter_title import alter_title
from src.main.media_metadata import MediaMetadata
from src.main.storage import AppStorage

def download_music(storage:AppStorage):
    info_list = storage.now_playing
    params = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(storage.get_user_music_path_choice(), '%(title)s.%(ext)s')
    }

    with YoutubeDL(params) as ydl:
        if info_list is not None:
            ydl.download([i.original_url for i in info_list if not _isExist(i)])


def _isExist(info_dict: MediaMetadata) -> bool:
    res = os.path.isfile(os.path.join(MUSIC_FOLDER,'{}.mp3'.format(alter_title(info_dict.title))))
    return res


