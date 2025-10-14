import asyncio

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    files = list_files(subtitle_dir, ".srt")
    await async_batch_exec(files, srt_to_txt)

if __name__ == "__main__":
    asyncio.run(main())
