import asyncio
import argparse

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    parser = argparse.ArgumentParser(description="*.res to *.ait")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="res filename suffix", default=".res")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix

    files = list_files(subtitle_dir, suffix)
    await async_batch_exec(files, res_to_ait)

if __name__ == "__main__":
    asyncio.run(main())
