import asyncio
import argparse

from common_util import *
from audio import *
from subtitle import *

async def main():
    parser = argparse.ArgumentParser(description="*.req to *.res")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="req filename suffix", default=".req")
    parser.add_argument("--batch_size", help="batch size", default="10")
    parser.add_argument("--base_url", help="ai chat base url", default="https://api.siliconflow.cn/v1")
    parser.add_argument("--api_key", help="api_key", default=f"{os.environ.get("OPENAI_API_KEY")}")
    parser.add_argument("--model", help="model", default="deepseek-ai/DeepSeek-V3.2-Exp")
    parser.add_argument("--topic", help="topic", default="Power Platform & Dynamics 365 CRM")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix
    batch_size=int(args.batch_size)
    base_url=args.base_url
    api_key=args.api_key
    model=args.model
    topic=args.topic

    files = list_files(subtitle_dir, suffix)
    for batch in batch_generator(files, batch_size):
        await async_batch_exec(batch, req_to_res, OpenAiChatClient(
            api_key=api_key,
            base_url=base_url,
            model=model,
            topic=topic,
        ), batch_size=len(batch))

if __name__ == "__main__":
    asyncio.run(main())
