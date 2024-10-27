import io
import os
import sys
import time
import urwid
import threading
from time import sleep
from songControl import *
import songControl as sC
from vars import *
import ytSearch as ytS
from youtube import MP3
from youtube import downloadFromlink as dfl

# Load global vars 
MP3.extension = PRIMARY_DOWNLOADING_FORMAT

def get_albums(music_directory):        return [d for d in os.listdir(music_directory) if os.path.isdir(os.path.join(music_directory, d))]
def get_songs(music_directory, album):  album_path = os.path.join(music_directory, album); return [os.path.join(album_path, f) for f in os.listdir(album_path) if f.endswith(FORMATES_TO_SHOW)]
def set_alarm(time, funtion_):          urwid.MainLoop(loop).set_alarm_in(time, funtion_)
def select_album(album, button):        current_album[0] = album; populate_song_list(song_list, music_directory, current_album[0])
def select_song(song, button):          play_audio(song); loop.set_alarm_in(UPDATE_INTERVAL, update_progress)

def populate_album_list(album_list, music_directory):
    albums = get_albums(music_directory)
    album_widgets = []
    for album in albums:
        button = urwid.Button(album)
        urwid.connect_signal(button, 'click', select_album, user_args=[album])
        album_widgets.append(urwid.AttrMap(button, 'button'))
    album_list.body = urwid.SimpleFocusListWalker(album_widgets)
def populate_song_list(song_list, music_directory, album):
    song_widgets = []
    if album:
        songs = get_songs(music_directory, album)
        for song in songs:
            song_name = os.path.basename(song)
            button = urwid.Button(song_name)
            urwid.connect_signal(button, 'click', select_song, user_args=[song])
            song_widgets.append(urwid.AttrMap(button, 'button'))
    ytS.stop = True
    song_list.body = urwid.SimpleFocusListWalker(song_widgets)
    songs_frame.body = urwid.LineBox(song_list, title= f'{album} - Songs')


def update_progress(loop=None, data=None):
    if sC.is_playing or sC.current_frame > 0:
        position = sC.current_frame / sC.stream.samplerate
        minutes, seconds = divmod(position, 60)
        total_minutes, total_seconds = divmod(sC.song_length, 60)

        max_width = os.get_terminal_size().columns // 2 - 30
        min_width = BAR_MIN_WIDTH
        progress_bar_width = max(min_width, max_width)

        filled_chars = int((position / sC.song_length) * progress_bar_width)
        empty_chars = progress_bar_width - filled_chars - BAR_INCOMPLETE_PLAYBACK_OFFSET # progress bar finish offset

        progress_text = f"[{BAR_FILED_CHAR * filled_chars}{BAR_PLAYER_MIDDLE}{BAR_EMPTY_CHAR * empty_chars}] {int(minutes)}:{int(seconds):02d} / {int(total_minutes)}:{int(total_seconds):02d}"
        progress_bar.set_text(progress_text)

    loop.set_alarm_in(UPDATE_INTERVAL, update_progress)


def key_binds(key):
    if key in   ('q', 'Q'):   raise urwid.ExitMainLoop()
    elif key in ('p', 'P'):   skip_backward()
    elif key in ('n', 'N'):   skip_forward()

def alarm_loop(loop, user_data=None):

    ...

    loop.set_alarm_in(1.0, alarm_loop)
    
music_directory = MUSIC_DIR  # music directory
current_album = [None]

# UI set up
album_list       = urwid.ListBox(urwid.SimpleFocusListWalker([]))
song_list        = urwid.ListBox(urwid.SimpleFocusListWalker([]))
song_list_search = urwid.ListBox(urwid.SimpleFocusListWalker([]))
populate_album_list(album_list, music_directory)

# Custom logging widget 
class PrintCapture(io.StringIO):
    def __init__(self, log_widget, loop):
        super().__init__()
        self.log_widget = log_widget
        self.loop = loop
        self.log_widget.body = urwid.SimpleFocusListWalker([])
        
    def write(self, s):
        if s.strip():
            self.log_widget.body.insert(0, urwid.Text(s.strip()))
            if len(self.log_widget.body) > LOGS_PANNEL_MAX_LOOGS:
                self.log_widget.body.pop()
            self.loop.draw_screen()
    def flush(self): pass

# Download Songs
def download_audio_THREAD(path, link, callback): info, audio_path = dfl.downloadAudio(path, link);callback(info, audio_path);
def download_callback(info, audio_path): threading.Thread(target=MP3.run_ffmpeg, args=[os.path.normpath(audio_path)]).start()
def download_audio(link, title, button):
    songs_frame.body = urwid.Pile([urwid.LineBox(urwid.Text(f"Downloading {title} . .. ", align='center'), title= 'Download')])
    ytS.stop = True
    loop.draw_screen()

    threading.Thread(target=download_audio_THREAD, args=[os.path.join(MUSIC_DIR, MUSIC_DIR_DOWNLOADS), link, download_callback]).start()
    showMenu = urwid.ListBox(urwid.SimpleFocusListWalker([]))
    songs_frame.body = showMenu
    sys.stdout = PrintCapture(showMenu, loop)
    
# Search bar
def populate_search_results(quary):
    ytS.refresh()
    results = dfl.search_(quary, limit= YT_MAX_RESULTS_SEARCH)
    results = results['result']
    buttons = ytS.create_video_buttons(results, download_audio)
    songs_frame.body = buttons
    loop.set_alarm_in(0.1, ytS.update_ascii_images, (buttons, results))

class _Edit_enterBlock(urwid.Edit):
    def keypress(self, size, key):
        if key == 'enter':
            searchBar_edit_on_enter(self)
            return None
        return super().keypress(size, key)

def searchBar_edit_on_change(searchBar_edit, new_edit_text): 
    searchBar_edit.set_caption("   Search " if new_edit_text == "" else "")
def searchBar_edit_on_enter(searchBar_edit):
    if searchBar_edit.get_edit_text() == "": return;
    songs_frame.body = urwid.Pile([urwid.LineBox(urwid.Text(f"getting results for {searchBar_edit.get_edit_text()} .. .", align='center'), title= 'result')])
    loop.draw_screen()
    populate_search_results(searchBar_edit.get_edit_text())

searchBar_edit = _Edit_enterBlock(caption="   Search", multiline=False)
urwid.connect_signal(searchBar_edit, 'change', searchBar_edit_on_change)
search_ = urwid.LineBox(searchBar_edit, title="")

# Button Funtions
def playerControls_Suffel(button)    : ...
def playerControls_Previouse(button) :    skip_backward()
def playerControls_Play(button)      :    pause_audio();   button.set_label(PLAY_BUTTON_LABLE_PLAY) if sC.is_playing else button.set_label(PLAY_BUTTON_LABLE_PAUSE)
def playerControls_Next(button)      :    skip_forward()
def playerControls_Repeat(button)    : ...

# Buttons
player_Controls_Suffel    = urwid.Button("[S]",                    align='center');   urwid.connect_signal(player_Controls_Suffel,    'click',  playerControls_Suffel)
player_Controls_Previouse = urwid.Button(SKIP_BACKWARD_LABLE,      align='center');   urwid.connect_signal(player_Controls_Previouse, 'click',  playerControls_Previouse)
player_Controls_Play      = urwid.Button(PLAY_BUTTON_LABLE_DEFULT, align='center');   urwid.connect_signal(player_Controls_Play,      'click',  playerControls_Play)
player_Controls_Next      = urwid.Button(SKIP_FORWARD_LABLE,       align='center');   urwid.connect_signal(player_Controls_Next,      'click',  playerControls_Next)
player_Controls_Repeat    = urwid.Button("[R]",                    align='center');   urwid.connect_signal(player_Controls_Repeat,    'click',  playerControls_Repeat)

# Song progress bar 
progress_bar = urwid.Text("No Songs Playing . .. ", align='center')

player_controls = urwid.Columns([
    ('weight', 1, player_Controls_Suffel),
    ('weight', 1, player_Controls_Previouse),
    ('weight', 1, player_Controls_Play),
    ('weight', 1, player_Controls_Next),
    ('weight', 1, player_Controls_Repeat)
])

player_ = urwid.Pile([
    urwid.LineBox(player_controls, title=""),
    urwid.LineBox(progress_bar, title="")
])
songs_frame = urwid.Frame(
    header  =   search_,
    body    =   urwid.LineBox(song_list, title="Songs"),
    footer  =   urwid.LineBox(player_, title="")
)

layout = urwid.Columns([
    ('weight', 1, urwid.LineBox(album_list, title="Albums")),
    ('weight', 2, songs_frame),
    ('weight', 1, urwid.LineBox(progress_bar, title="Progress"))
])
screen = urwid.raw_display.Screen()
main_frame = urwid.Frame(header=urwid.Text("Project TM"), body=layout)
loop = urwid.MainLoop(main_frame, unhandled_input=key_binds, screen=screen)
loop.set_alarm_in(1.0, alarm_loop)

loop.run() if __name__ == '__main__' else ...
def Run():                         loop.run()