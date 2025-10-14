import asyncio
import argparse

from common_util import *
from audio import *

async def audio_to_audio(input_path, to_ext="wav"):
    if input_path.endswith(to_ext): return input_path
    output_path = with_ext(input_path, to_ext)
    await audio_convert(input_path, output_path)

async def main():
    parser = argparse.ArgumentParser(description="audio convert")
    parser.add_argument("--audio_dir", help="audio directory", default="audios")
    parser.add_argument("-f", help="audio from type", default="mp3")
    parser.add_argument("-t", help="audio to type", default="wav")
    args = parser.parse_args()

    audio_dir=args.audio_dir
    suffix=args.f
    to_ext=args.t

    files = list_files(audio_dir, suffix)
    await async_batch_exec(files, audio_to_audio, to_ext)

if __name__ == "__main__":
    asyncio.run(main())
