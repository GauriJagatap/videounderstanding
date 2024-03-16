'''
script to extract clips from list of start and end indices of a given video and save clips
'''

import os, argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--videopath", default='./videos/video.mp4')
    parser.add_argument("--savedir",default='./editedclips')
    parser.add_argument("--timestamps", type=int, nargs="+", default=None)
    parser.add_argument("--combine", action="store_true")

    args = parser.parse_args()

    if not os.path.exists(args.savedir):
        os.mkdir(args.savedir)

    filename = os.path.basename(args.videopath)[:-4]    
    video = VideoFileClip(args.videopath)
    
    chunks = int(video.duration // 150) + 1
    print(chunks)

    if not args.timestamps:
        timearray = [[150 * i, 150 * (i+1)] for i in range(chunks-1)]
        x = [[150 * (chunks-1), int(video.duration)]]
        timearray = timearray + x

    else:
        timearray = np.reshape(args.timestamps, (int(len(args.timestamps)/2),2))

    cliparray = []

    for i,cliptime in enumerate(timearray):
        
        clip = video.subclip(cliptime[0],cliptime[1])
        clip.write_videofile(os.path.join(args.savedir,filename+"_clip_"+str(i+1)+".mp4"))
        cliparray.append(clip)

    if args.combine:
        combinedvid = concatenate_videoclips(cliparray)
        combinedvid.write_videofile(os.path.join(args.savedir,filename+"_edited.mp4"))

if __name__ == "__main__":
    main()    
