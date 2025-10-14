import asyncio
import argparse

from functools import partial

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def srt_to_audio(srt_path, voice):
    audio_name = with_ext(path.basename(srt_path), "mp3")
    audio_path = project_resolve(audio_dir, audio_name)
    return await srt_to_mp3(srt_path, audio_path, voice, delete_ais=True)

async def main():
    parser = argparse.ArgumentParser(description="ais to mp3")
    parser.add_argument("suffix", help="srt file suffix: zh.ais, zh.srt", default="zh.ais")
    args = parser.parse_args()

    files = list_files(subtitle_dir, args.suffix)
    await async_batch_exec(files, srt_to_audio, "zh-CN-XiaoxiaoNeural")

if __name__ == "__main__":
    asyncio.run(main())
