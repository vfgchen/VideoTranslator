import asyncio
import argparse

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    parser = argparse.ArgumentParser(description="*.txt to *.req")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default=f"{subtitle_dir}")
    parser.add_argument("--suffix", help="txt filename suffix", default=".txt")
    parser.add_argument("--topic", help="topic", default="Power Platform PL-100")
    args = parser.parse_args()

    files = list_files(args.subtitle_dir, args.suffix)
    await async_batch_exec(files, txt_to_req, args.topic)

if __name__ == "__main__":
    asyncio.run(main())
