import yt_dlp
from youtubesearchpython import VideosSearch

def downloadAudio(save_path, link):
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': f"{save_path}\\%(title)s.%(ext)s",
        'progress_hooks': [lambda d: log_message(f"Status: {d['status']} - {d.get('filename', 'N/A')}")],
    }
    try:
        log_message(f"Downloading audio to: {save_path}")
        with yt_dlp.YoutubeDL(ydl_opts_audio) as ydl:
            info_video = ydl.extract_info(link, download=True)
            audio_path = f"{save_path}/{info_video['title']}.{info_video['ext']}"
            log_message(f"Downloaded: {audio_path}")
            return [info_video, audio_path]
    except Exception as e:
        log_message(f"An error occurred while downloading: {e}")

def log_message(mg): print(mg)

def search_(query, limit = 2):
    videos_search = VideosSearch(query, limit=limit)
    results = videos_search.result()
    return results
