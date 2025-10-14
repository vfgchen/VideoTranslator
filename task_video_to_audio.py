import asyncio
import argparse

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
    parser = argparse.ArgumentParser(description="video to audio")
    parser.add_argument("--suffix", help="video filename suffix", default="en.mp4")
    parser.add_argument("--to_ext", help="to audio type", default="mp3")
    args = parser.parse_args()

    files = list_files(video_dir, args.suffix)
    await async_batch_exec(files, video_to_audio, args.to_ext)

if __name__ == "__main__":
    asyncio.run(main())
