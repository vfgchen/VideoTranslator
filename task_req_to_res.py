import asyncio
import argparse

from functools import partial

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    parser = argparse.ArgumentParser(description="deepseek req to res")
    parser.add_argument("api_key", help="api_key", default="")
    args = parser.parse_args()

    files = list_files(subtitle_dir, ".req")
    for batch in batch_generator(files, batch_size=10):
        await async_batch_exec(batch, req_to_res, DeepseekTxtTranslator(
            api_key=args.api_key,
            base_url="https://api.siliconflow.cn/v1",
            model="deepseek-ai/DeepSeek-V3.2-Exp",
            topic="Power Platform PL-100",
        ), batch_size=len(batch))

if __name__ == "__main__":
    asyncio.run(main())
