import asyncio

from util import *
from audio import *
from openai_whisper import *

async def audio_to_subtitle(audio_path, recognizer: AudioRecognizer):
    srt_name = with_ext(path.basename(audio_path), "srt")
    srt_path = project_resolve(subtitle_dir, srt_name)
    await audio_to_srt(audio_path, srt_path, recognizer)

async def main():
    files = list_files(audio_dir, ".mp3")
    await async_batch_exec(files, audio_to_subtitle, WhisperAudioRecognizer(model_name="medium"))

if __name__ == "__main__":
    asyncio.run(main())
