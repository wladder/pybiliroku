# -*- coding:utf-8 -*-
import os
import datetime
from collections import defaultdict
from utils import *

videos = get_videos()
videos = videos_with(videos, _with=[".flv", ".ass"], _without=[".mp4"])
if videos.items():
    video_list = list(videos.values())[0]

    if video_list:
        video = video_list[0]

        if os.name == 'posix':
            with open(f'{video.path_without_ext}.ass') as inp:
                with open(f'temp.ass', 'w') as out:
                    out.write(inp.read().replace('黑体', 'WenQuanYi Micro Hei'))
        else:
            with open(f'{video.path_without_ext}.ass', encoding='utf-8') as inp:
                with open(f'temp.ass', 'w', encoding='utf-8') as out:
                    out.write(inp.read())

        scale = '1280:720'
        bitrate = '1500k'
        #scale = '852:480'
        #bitrate = '1200k'
        #scale = '1920:1080'
        #bitrate = '5900k'
        cmd = (f'{ffmpeg} -analyzeduration 2147483647 -probesize 2147483647 -y -f live_flv -i "{video.path_without_ext}.flv" -vf "subtitles=temp.ass, scale={scale}" -c:v libx264 -preset veryfast -b:v {bitrate} -c:a aac -b:a 128k -r 30 -max_muxing_queue_size 20000 "{video.path_without_ext}.mp4"')
        os_system_ensure_success(cmd)
        move_to_trash(f'{video.path_without_ext}.flv')
        move_to_trash(f'{video.path_without_ext}.ass')

