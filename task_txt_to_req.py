import asyncio

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    files = list_files(subtitle_dir, "123*.txt")
    await async_batch_exec(files, txt_to_req, "Power Platform PL-100")

if __name__ == "__main__":
    asyncio.run(main())
