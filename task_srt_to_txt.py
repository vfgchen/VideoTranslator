import asyncio
import argparse

from common_util import *
from audio import *
from subtitle import *

async def main():
    parser = argparse.ArgumentParser(description="*.srt to *.txt")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="res filename suffix", default=".srt")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix

    files = list_files(subtitle_dir, suffix)
    await async_batch_exec(files, srt_to_txt)

if __name__ == "__main__":
    asyncio.run(main())
