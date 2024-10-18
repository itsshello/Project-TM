import os
import urwid
import pygame
from songControl import *
import songControl as sC
from vars import *


def get_albums(music_directory):        return [d for d in os.listdir(music_directory) if os.path.isdir(os.path.join(music_directory, d))]
def get_songs(music_directory, album):  album_path = os.path.join(music_directory, album); return [os.path.join(album_path, f) for f in os.listdir(album_path) if f.endswith(('.mp3', '.wav', '.flac'))]
def set_alarm(time, funtion_):          urwid.MainLoop(loop).set_alarm_in(time, funtion_)
def select_album(album, button):        current_album[0] = album; populate_song_list(song_list, music_directory, current_album[0])

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
    song_list.body = urwid.SimpleFocusListWalker(song_widgets)

def select_song(song, button):
    play_audio(song)
    loop.set_alarm_in(UPDATE_INTERVAL, update_progress)


def update_progress(loop=None, data=None):
    if sC.is_playing:
        position = sC.pygame.mixer.music.get_pos() // 1000
        minutes, seconds = divmod(position, 60)
        total_minutes, total_seconds = divmod(sC.song_length, 60)

        max_width = loop.screen.get_cols_rows()[0] // 2 - 30
        progress_bar_width = max(10, max_width)

        filled_chars = int((position / sC.song_length) * progress_bar_width)
        empty_chars = progress_bar_width - filled_chars

        progress_text = f"[{'=' * filled_chars}{'-' * empty_chars}] {int(minutes)}:{int(seconds):02d} / {int(total_minutes)}:{int(total_seconds):02d}"
        progress_bar.set_text(progress_text)

    loop.set_alarm_in(UPDATE_INTERVAL, update_progress)



def key_binds(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif key in ('p', 'P'):
        skip_backward()
    elif key in ('n', 'N'):
        skip_forward()

def alarm_loop(loop, user_data=None):

    ...

    loop.set_alarm_in(1.0, alarm_loop)
    
music_directory = MUSIC_DIR  # music directory
current_album = [None]

# UI set up
album_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
song_list = urwid.ListBox(urwid.SimpleFocusListWalker([]))
populate_album_list(album_list, music_directory)

# Search bar
def on_change(searchBar_edit, new_edit_text): searchBar_edit.set_caption("   Search") if new_edit_text == "" else searchBar_edit.set_caption("")
searchBar_edit = urwid.Edit(caption="   Search", multiline=False)
urwid.connect_signal(searchBar_edit, 'change', on_change)
search_ = urwid.LineBox(searchBar_edit, title="")

# Button Funtions
def playerControls_Suffel(button): ...
def playerControls_Previouse(button):    skip_backward()
def playerControls_Play(button):         pause_audio()
def playerControls_Next(button):         skip_forward()
def playerControls_Repeat(button): ...

# Buttons
player_Controls_Suffel = urwid.Button("[S]");      urwid.connect_signal(player_Controls_Suffel, 'click', playerControls_Next)
player_Controls_Previouse = urwid.Button("[P]");   urwid.connect_signal(player_Controls_Previouse, 'click', playerControls_Next)
player_Controls_Play = urwid.Button("[Play]");     urwid.connect_signal(player_Controls_Play, 'click', playerControls_Play)
player_Controls_Next = urwid.Button("[N]");        urwid.connect_signal(player_Controls_Next, 'click', playerControls_Next)
player_Controls_Repeat = urwid.Button("[R]");      urwid.connect_signal(player_Controls_Repeat, 'click', playerControls_Next)

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
    header= search_,
    body=urwid.LineBox(song_list, title="Songs"),
    footer=urwid.LineBox(player_, title="")
)

layout = urwid.Columns([
    ('weight', 1, urwid.LineBox(album_list, title="Albums")),
    ('weight', 2, songs_frame),
    ('weight', 1, urwid.LineBox(progress_bar, title="Progress"))
])

main_frame = urwid.Frame(header=urwid.Text("Project TM"), body=layout)
loop = urwid.MainLoop(main_frame, unhandled_input=key_binds)
loop.set_alarm_in(1.0, alarm_loop)

loop.run() if __name__ == '__main__' else ...
def Run():                         loop.run()