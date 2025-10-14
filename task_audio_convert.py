import asyncio
import argparse

from util import *
from audio import *

async def audio_to_audio(input_path, to_ext="wav"):
    if input_path.endswith(to_ext): return input_path
    output_path = with_ext(input_path, to_ext)
    await audio_convert(input_path, output_path)

async def main():
    parser = argparse.ArgumentParser(description="audio convert")
    parser.add_argument("--suffix", help="audio filename suffix", default="mp3")
    parser.add_argument("--to_ext", help="to audio type", default="wav")
    args = parser.parse_args()

    files = list_files(audio_dir, args.suffix)
    await async_batch_exec(files, audio_to_audio, args.to_ext)

if __name__ == "__main__":
    asyncio.run(main())
