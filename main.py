from bin import init
from youtube import downloadFromlink as dfl
from youtube import MP3
from os import path as p
from UI import Run

def ABS(path_):
    if path_.startswith(('/', '\\')):
        path_ = path_[1:]
    path_ = p.normpath(path_)
    current_dir = p.realpath('.')
    return p.join(current_dir, path_)


if __name__ == '__main__':
    # MP3.toMP3(ABS('/songs/Discord’s Discovery Feature is perfectly balanced....webm'))
    Run()
