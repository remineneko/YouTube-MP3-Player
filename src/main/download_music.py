from yt_dlp import YoutubeDL
from typing import Dict
from settings import *


def download_music(info_dict: Dict = None, info_list = None):
    params = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(MUSIC_FOLDER, '%(title)s.%(ext)s')
    }

    with YoutubeDL(params) as ydl:
        if info_list is not None:
            ydl.download([i['original_url'] for i in info_list if not _isExist(i)])
        elif info_dict is not None:
            if not _isExist(info_dict):
                ydl.download([info_dict['original_url']])


def _isExist(info_dict) -> bool:
    res = os.path.isfile(os.path.join(MUSIC_FOLDER,'{}.mp3'.format(alter_title(info_dict['title']))))
    print(res)
    return res

def alter_title(title):
    illegal = ["\\", ":", "<", ">", "\"", "/", "|", "?", "*"]
    for restriction in illegal:
        title = title.replace(restriction, "_")
    print(title)
    return title