#                     WARNING 
# This is in python so DO NOT DOWNLOAD RANDOM 'vars.py' FILE 
# ANY CODE ON THIS FILE WILL BE RAN ON THE START OF THE PLAYER
# CHANGE VALUES DO NOT CHANGE THE WHOLE FILE UNLESS YOU KNOW WHAT YOU ARE DOING

# Progress bar 
UPDATE_INTERVAL = 0.5
BAR_MIN_WIDTH   = 10
BAR_FILED_CHAR    = '='
BAR_EMPTY_CHAR    = '-'
BAR_PLAYER_MIDDLE = '0' # set to '' if you want no middle else set it to a char like '0' or '|'
BAR_INCOMPLETE_PLAYBACK_OFFSET = 0

# Music
MUSIC_DIR = 'songs'                # DONT ADD '/' or '\' INFORNT OF RELATIVE PATHS  [Music folder]
MUSIC_DIR_DOWNLOADS = 'downloads'  # DONT ADD '/' or '\' INFORNT OF RELATIVE PATHS  [Music album ]
FORMATES_TO_SHOW = ('.mp3', '.wav', '.flac', '.ogg', '.aiff', '.au') # remove mp3 if it does not work

# Song play back 
BOTH_SKIPS = 10               # 10 sec
SKIP_FORWARD  = BOTH_SKIPS    # Set it to a number to customize [ sec ]
SKIP_BACKWARD = BOTH_SKIPS    # Set it to a number to customize [ sec ]

# Search
YT_MAX_RESULTS_SEARCH = 10    # Set it high or less to get more or less results
IMAGE_THUMNAIL_ASKII  = False

# System 
LOGS_PANNEL_MAX_LOOGS = 40

# Download                   [Note: some format can be unsupported, supported formats are wav, flac, ogg, aiff, au]
# Because the player depends on soundfile to read it which uses libsndfile, so thoes formats can be unsupported
# Also mp3 is not listed because it is not supported for every device, also soundfile dosent even say mp3 on the main page 
PRIMARY_DOWNLOADING_FORMAT = 'wav'

# ASKII Art 
ASKII_ART_STR_MAP = " .:-=+*#%@"

# Key Binds 
# some of the Key Binds are not customize able
# so they are not inculded