import asyncio
import argparse

from util import *
from video import *

async def video_to_namp4(video_path):
    namp4_path = video_path.split("-")[0] + "-na.mp4"
    await video_to_na_mp4(video_path, namp4_path)

async def main():
    parser = argparse.ArgumentParser(description="video to *-na.mp4")
    parser.add_argument("--video_dir", help="video directory", default=f"{video_dir}")
    parser.add_argument("--suffix", help="video filename suffix", default=".mp4")
    args = parser.parse_args()

    files = list_files(args.video_dir, args.suffix)
    await async_batch_exec(files, video_to_namp4)

if __name__ == "__main__":
    asyncio.run(main())
