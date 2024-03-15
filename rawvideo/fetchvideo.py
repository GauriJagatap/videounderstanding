'''
script to fetch video from youtube url
'''
import argparse
from pytube import YouTube
import os


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--url',type=str,help="YT URL",default='https://www.youtube.com/watch?v=JPx2M6FzdqQ')
    parser.add_argument('--save_path',type=str,default='./videos')

    args = parser.parse_args()

    textpath = os.path.join(os.path.dirname(os.path.normpath(args.save_path)),'texts')
    if not os.path.exists(args.save_path):
        os.mkdir(args.save_path)
    if not os.path.exists(textpath):
        os.mkdir(textpath)        

    try:
        yt = YouTube(args.url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=args.save_path)
    except Exception as e:
        print(f'Exception: {e}')         

    vidtextpath = os.path.join(textpath,yt.title+'.txt')
    with open(vidtextpath,"w") as file:    
        file.write(yt.description)

if __name__ == "__main__":
    main()    

