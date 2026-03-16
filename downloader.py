import yt_dlp

def download_audio(url):

    ydl_opts={
        'format':'bestaudio/best',
        'outtmpl':'song.%(ext)s'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info=ydl.extract_info(url,download=True)

        return ydl.prepare_filename(info)