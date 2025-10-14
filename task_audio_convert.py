import asyncio

from util import *
from audio import *

async def audio_to_audio(input_path, to_ext="wav"):
    if input_path.endswith(to_ext): return input_path
    output_path = with_ext(input_path, to_ext)
    await audio_convert(input_path, output_path)

async def main():
    files = list_files(audio_dir, ".mp3")
    await async_batch_exec(files, audio_to_audio)

if __name__ == "__main__":
    asyncio.run(main())
