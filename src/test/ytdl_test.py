from yt_dlp import YoutubeDL

inst = YoutubeDL()

norm_url = "youtu.be/ETGWiArNaO0"
playlist_url = "https://www.youtube.com/watch?v=O6vqvlHwkxk&list=PLj3JxVDwUCBlJEZ33x5vSjCCEnJImg1js"

print(inst.extract_info(norm_url, download = False).keys())
print(inst.extract_info(playlist_url, download = False)['entries'])