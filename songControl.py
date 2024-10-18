import pygame
from vars import *
# import test

pygame.mixer.init()

current_song = None
is_playing = False
song_length = 0

def change_current_song(song_): global current_song; current_song = song_

def play_audio(song_path):
    global is_playing, song_length, current_song
    if current_song != song_path:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        is_playing = True
        song_length = pygame.mixer.Sound(song_path).get_length()
        current_song = song_path

def pause_audio():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
        is_playing = False
    else:
        pygame.mixer.music.unpause()
        is_playing = True

def skip_forward():
    position = pygame.mixer.music.get_pos() // 1000 
    new_position = position + 100
    if new_position < song_length:
        pygame.mixer.music.rewind()
        pygame.mixer.music.set_pos(new_position)

def skip_backward():
    position = pygame.mixer.music.get_pos() // 1000
    new_position = max(0, position - 100)
    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(new_position)
