import asyncio

from util import *
from video import *

async def video_to_audio(video_path, ext="mp3"):
    audio_name = with_ext(path.basename(video_path), ext)
    audio_path = project_resolve(audio_dir, audio_name)
    if ext == "mp3":
        return await video_to_mp3(video_path, audio_path)
    else:
        return await video_to_wav(video_path, audio_path)

async def main():
    files = list_files(video_dir, "en.mp4")
    await async_batch_exec(files, video_to_audio)

if __name__ == "__main__":
    asyncio.run(main())
