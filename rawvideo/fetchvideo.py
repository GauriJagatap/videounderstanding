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
    if not os.path.exists(args.save_path):
        os.mkdir(args.save_path)

    try:
        yt = YouTube(args.url)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=args.save_path)
    except Exception as e:
        print(f'Exception: {e}')        


if __name__ == "__main__":
    main()    

