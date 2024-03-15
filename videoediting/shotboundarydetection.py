'''
script to automatically identify scene changes
'''
from scenedetect import detect, AdaptiveDetector, split_video_ffmpeg
import argparse
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videopath",type=str,default='./videos')
    parser.add_argument("--savepath",type=str,default='./videoclips')

    args = parser.parse_args()

    if not os.path.exists(args.savepath):
        os.mkdir(args.savepath)

    videopaths = os.listdir(args.videopath)
    for videopath in videopaths:
        filenameroot = videopath[:-4]
        fullvideopath = os.path.join(args.videopath,videopath)
        print(fullvideopath)
        scene_list = detect(fullvideopath,detector=AdaptiveDetector())
        split_video_ffmpeg(fullvideopath,scene_list,args.savepath)

if __name__ == "__main__":
    main()    