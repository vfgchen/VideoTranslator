import asyncio
import argparse

from util import *
from video import *

async def video_to_namp4video(video_path):
    video_dir = path.dirname(video_path)
    namp4_name = path.basename(video_path).split("-")[0] + "-na.mp4"
    namp4_path = path.join(video_dir, namp4_name)
    await video_to_namp4(video_path, namp4_path)

async def main():
    parser = argparse.ArgumentParser(description="video to *-na.mp4")
    parser.add_argument("--video_dir", help="video directory", default="videos")
    parser.add_argument("--suffix", help="video filename suffix", default="mp4")
    args = parser.parse_args()

    video_dir=args.video_dir
    suffix=args.suffix

    files = list_files(video_dir, suffix)
    await async_batch_exec(files, video_to_namp4video)

if __name__ == "__main__":
    asyncio.run(main())
