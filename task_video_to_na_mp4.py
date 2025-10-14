import asyncio

from util import *
from video import *

async def video_to_namp4(video_path):
    namp4_path = video_path.split("-")[0] + "-na.mp4"
    await video_to_na_mp4(video_path, namp4_path)

async def main():
    files = list_files(video_dir, ".mp4")
    await async_batch_exec(files, video_to_namp4)

if __name__ == "__main__":
    asyncio.run(main())
