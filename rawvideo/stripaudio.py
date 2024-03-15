'''
script to strip audio from video 
'''
import argparse
import os
from moviepy.editor import VideoFileClip

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--video_dir",default="./videos",type=str)
    parser.add_argument("--audio_dir",default="./audios",type=str)

    args = parser.parse_args()

    videopaths = os.listdir(args.video_dir)

    if not os.path.exists(args.audio_dir):
        os.mkdir(args.audio_dir)
        
    for videopath in videopaths:
        video = VideoFileClip(os.path.join(args.video_dir,videopath))
        audio = video.audio
        audio.write_audiofile(os.path.join(args.audio_dir,videopath[:-3]+'mp3'))

if __name__ == "__main__":
    main()