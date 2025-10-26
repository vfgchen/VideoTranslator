import asyncio
import argparse

from common_util import *
from audio import *
from subtitle import *

async def main():
    parser = argparse.ArgumentParser(description="*.txt to *.req")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="txt filename suffix", default=".txt")
    parser.add_argument("--topic", help="topic", default="Dynamics 365 CRM")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix
    topic=args.topic

    files = list_files(subtitle_dir, suffix)
    await async_batch_exec(files, txt_to_req, topic)

if __name__ == "__main__":
    asyncio.run(main())
