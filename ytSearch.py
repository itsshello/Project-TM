import urwid
from PIL import Image
import os
import requests
from io import BytesIO
import json
from vars import *

width__ = os.get_terminal_size().columns
stop    = False

def image_to_ascii(url, width=50):
    try:
        response     =  requests.get(url)
        img          =  Image.open(BytesIO(response.content))
        aspect_ratio =  img.height / img.width
        new_height   =  int(aspect_ratio * width * 0.55)
        img          =  img.resize((width, new_height))
        img          =  img.convert('L')

        chars     = ASKII_ART_STR_MAP
        pixels    = img.getdata()
        ascii_str = "".join([chars[pixel // 25] for pixel in pixels])

        ascii_img = "\n".join([ascii_str[i:i + width] for i in range(0, len(ascii_str), width)])
        return ascii_img

    except Exception as e:
        return "[Image not available]"

def update_ascii_image_in_placeholder(text_widget, thumbnail_url, size):
    width = max(20, int(size[0]/2))
    if width <= 50: width = int(size[0]/5);
    if width >= 50: width = int(size[0]/7);

    ascii_image = image_to_ascii(thumbnail_url, width=width)
    if not isinstance(text_widget, urwid.WidgetPlaceholder):
        text_widget.set_text(ascii_image)

askii_text_widget = []
def create_video_buttons(results, callback_):
    global width__
    buttons = []
    for video in results:
        title              =  str(video.get('title', 'No Title'))
        duration           =  str(video.get('duration', 'Unknown Duration'))
        publishedTime      =  str(video.get('publishedTime', 'Unknown Date'))
        viewCount          =  str(video.get('viewCount', {}).get('short', 'No Views'))
        channel_name       =  str(video.get('channel', {}).get('name', 'Unknown Channel'))
        descriptionSnippet = (str(video.get('descriptionSnippet', [{}])[0].get('text')) if video.get('descriptionSnippet') else 'No Description')
        link               =  str(video.get('link', 'No Link'))
        thumbnail_url      =  str(video.get('thumbnails', [{}])[0].get('url', 'No Thumbnail'))

        clickable_button   = urwid.Button(label="")
        urwid.connect_signal(clickable_button, 'click', callback_, user_args=[link, title])

        image_askii_text = urwid.Text('Loading image...') 
        askii_text_widget.append(image_askii_text)
        ascii_image_placeholder = urwid.WidgetPlaceholder(image_askii_text)
        size = (80, 24)  # Default terminal size
        update_ascii_image_in_placeholder(ascii_image_placeholder, thumbnail_url, size)
        video_description = urwid.Text(
            f"{title}\n"
            f"{duration} | {publishedTime} | {viewCount}\n"
            f"{channel_name}\n"
            f"{descriptionSnippet}"
        )

        video_info = urwid.Columns([
            ('weight', 3, ascii_image_placeholder),
            ('weight', 5, video_description)
        ])

        lineBox_            = urwid.LineBox(video_info, title="")
        button_placeholder  = urwid.AttrMap(lineBox_, None)
        clickable_button._w = button_placeholder
        buttons.append(clickable_button)

    width__ = 0
    return urwid.ListBox(urwid.SimpleFocusListWalker(buttons))

def update_ascii_images(loop, user_data):
    global stop, width__
    video_buttons, youtube_data = user_data
    if not width__ == os.get_terminal_size().columns:
        width__ = os.get_terminal_size().columns
        size = loop.screen.get_cols_rows()

        for idx, button in enumerate(video_buttons.body):
            thumbnail_url = youtube_data[idx]['thumbnails'][0]['url']
            if len(askii_text_widget) > idx: update_ascii_image_in_placeholder(askii_text_widget[idx], thumbnail_url, size)
    if stop: stop = False
    else:    loop.set_alarm_in(1, update_ascii_images, (video_buttons, youtube_data))

def refresh():
    global width__, stop, askii_text_widget
    width__           = 0
    stop              = False
    askii_text_widget = []