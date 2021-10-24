# YouTube-MP3-Player
a simple app to play audio from YouTube and BiliBili videos.

# Requirements to run the scripts
- [Python 3.6+](https://www.python.org/downloads/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [ffmpeg](https://www.ffmpeg.org/) (for yt-dlp)
- [PyQt5](https://pypi.org/project/PyQt5/)
- [requests](https://pypi.org/project/requests/)

# Running the scripts
Just run ```main.py```

# Using the app
1. You can put in any valid YouTube/Bilibili link, and then click on Load to load the metadata of the video(s) provided by the link. 
Multiple links as input is not supported at the moment.

2. To play all songs, press Play. 
To play selected videos, press Play then click on Play Selected. 
The MP3 files for the videos will be downloaded, by default, at YouTube-MP3-Player/data/now_playing. 
You can change this directory at Settings

3. To save the current list of videos in the main menu, click on Save Playlist. 
By default, the app will redirect itself to YouTube-MP3-Player/data/SavedPlaylists. 
You can change this directory at Settings.
When the playlist is saved, a .json file will be created, with each entry (each video saved in playlist is regarded as an entry) will be saved as follows:
```
{
    "title": , 
    "duration": , 
    "url": 
}
```

4. To load a saved playlist, click on Load Playlist.

5. To add a video that is not in the playlist shown in Main Menu, click on Add. 
There are three options:
+ Add songs via links. You can add multiple YouTube/BiliBili links, seperated by ```;```, then click on Add Songs
+ Add songs via search. You can search for videos, currently either on YouTube or Bilibili, then have the results be added to the main playlist.
Currently the search limit is 20 per query, but a way to modify this will be added soon.
+ Add songs via a different playlist. You can load a different playlist, then have it added to the main playlist. 
Currently, all songs from the playlist will be added, but the choice to select songs to add from playlist will be added soon.

6. You can remove songs - select one or more songs at the main menu to remove them.

7. You can modify some settings. 
Aside from aforementioned settings, you can also select whether you want all of the downloaded MP3 to be deleted after the app session is over. 
Removal of individual songs will be added soon.

# Miscellaneous
- You can double click on videos in Main Menu and Search to see more information about the video, though at the moment very simple data is presented.
