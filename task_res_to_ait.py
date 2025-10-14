import asyncio
import argparse

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    files = list_files(subtitle_dir, ".res")
    await async_batch_exec(files, res_to_ait)

if __name__ == "__main__":
    asyncio.run(main())
