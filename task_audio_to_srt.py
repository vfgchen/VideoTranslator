import asyncio
import argparse

from common_util import *
from audio import *
from openai_whisper import *
from openai_sensevoice import *

async def audio_to_subtitle(audio_path, recognizer: AudioRecognizer):
    srt_name = with_ext(path.basename(audio_path), "srt")
    srt_path = project_resolve(subtitle_dir, srt_name)
    await audio_to_srt(audio_path, srt_path, recognizer, delete_audio=True)

async def main():
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--audio_dir", help="audio directory", default="audios")
    parser.add_argument("--suffix", help="audio filename suffix", default=".mp3")
    parser.add_argument("--recognizer", help="audio recognizer", choices=["whisper", "sensevoice"], default="sensevoice")
    parser.add_argument("--model_name", help="whisper model name", default="medium")
    args = parser.parse_args()

    audio_dir=args.audio_dir
    suffix=args.suffix
    model_name=args.model_name
    recognizer=args.recognizer.lower()

    # audio recognizer
    if recognizer == "whisper":
        audio_recognizer = WhisperAudioRecognizer(model_name=model_name)
    elif recognizer == "sensevoice":
        audio_recognizer = SenseVoiceAudioRecognizer()
    else:
        raise "please setup audio recognizer"

    files = list_files(audio_dir, suffix)
    await async_batch_exec(files,
                           audio_to_subtitle,
                           audio_recognizer,
                           batch_size=1) # 语音识别只能一次一个执行，并行会报错

if __name__ == "__main__":
    asyncio.run(main())
