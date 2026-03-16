import yt_dlp

def search_music(query):

    ydl_opts={'quiet':True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info=ydl.extract_info(f"ytsearch10:{query}",download=False)

    return info['entries']