import asyncio

from functools import partial

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def srt_to_audio(srt_path, voice):
    audio_name = with_ext(path.basename(srt_path), "mp3")
    audio_path = project_resolve(audio_dir, audio_name)
    return await srt_to_mp3(srt_path, audio_path, voice)

async def main():
    files = list_files(subtitle_dir, ".srt")
    await async_batch_exec(files, srt_to_audio, "zh-CN-XiaoxiaoNeural")

if __name__ == "__main__":
    asyncio.run(main())
