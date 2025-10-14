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
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="srt file suffix: zh.ais, zh.srt", default="zh.ais")
    parser.add_argument("--voice", help="dubbing voice", default="zh-CN-XiaoxiaoNeural")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix
    voice=args.voice

    files = list_files(subtitle_dir, suffix)
    await async_batch_exec(files, srt_to_audio, voice)

if __name__ == "__main__":
    asyncio.run(main())
