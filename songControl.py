import sounddevice as sd
import soundfile as sf
import numpy as np
from vars import *

current_song = None
is_playing = False
song_length = 0
audio_data = None
current_frame = 0
stream = None

def change_current_song(song_): global current_song; current_song = song_

def play_audio(song_path):
    global is_playing, song_length, current_song, audio_data, stream, current_frame
    if current_song != song_path:
        if stream:
            stream.stop()
        audio_data, sample_rate = sf.read(song_path, dtype='float32')
        song_length = len(audio_data) / sample_rate
        current_song = song_path
        current_frame = 0

        stream = sd.OutputStream(samplerate=sample_rate, channels=audio_data.shape[1], callback=callback)
        stream.start()

        is_playing = True

def callback(outdata, frames, time, status):
    global current_frame, audio_data
    if not is_playing:
        outdata[:] = np.zeros_like(outdata)
        return
    chunk = audio_data[current_frame:current_frame + frames]
    outdata[:len(chunk)] = chunk
    # End of the song*
    if len(chunk) < frames:
        outdata[len(chunk):] = 0
        stop_audio()
    current_frame += frames

def pause_audio():
    global is_playing
    if     is_playing : is_playing = False
    else:  is_playing = True

def skip_forward():
    global current_frame, song_length, audio_data
    sample_rate = stream.samplerate
    new_frame = current_frame + int(sample_rate * SKIP_FORWARD)

    if new_frame < len(audio_data): current_frame = new_frame

def skip_backward():
    global current_frame
    sample_rate = stream.samplerate
    current_frame = max(0, current_frame - int(sample_rate * SKIP_BACKWARD))

def stop_audio():
    global is_playing, stream
    is_playing = False
    if stream: stream.stop()
