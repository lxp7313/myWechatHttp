import os
import you-get

def download_videos(video_list):
    for video in video_list:
        os.system('you-get {}'.format(video))

if __name__ == '__main__':
    video_list = [
        "https://v.youku.com/v_show/id_XMjcxOTg4ODcyNA==.html?playMode=pugv&frommaciku=1"
    ]
    download_videos(video_list)

