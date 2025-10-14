import asyncio
import argparse

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    parser = argparse.ArgumentParser(description="*.ait check")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="req filename suffix", default=".ait")
    args = parser.parse_args()

    subtitle_dir = args.subtitle_dir
    suffix = args.suffix

    ait_check_err = path.join(subtitle_dir, "ait_check.err")
    if path.exists(ait_check_err):
        os.remove(ait_check_err)

    files = list_files(subtitle_dir, suffix)
    results = await async_batch_exec(files, ait_check)
    lines = [err_info for match, err_info in results if not match]
    if len(lines) == 0:
        print(f"success, all is match ...")
        return
    await write_lines(ait_check_err, lines)

if __name__ == "__main__":
    asyncio.run(main())
