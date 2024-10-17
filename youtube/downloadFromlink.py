import yt_dlp

def downloadAudio(save_path, link):
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': save_path + '/%(title)s.%(ext)s',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            print(f"Downloading Audio at: \n {save_path}")
            info_video = ydl.extract_info(link, download=True)
            audio_path = f"{save_path}/{info_video['title']}.{info_video['ext']}"
            return [info_video, audio_path]
    except Exception as e:
        print(f"An Error occurred while Downloading: \n {e}")