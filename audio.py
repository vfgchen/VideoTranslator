import pysrt

from util import *

async def audio_convert(input: str, output: str) -> str:
    """
    音频格式转换: mp3 <=> wav
    ffmpeg -y -i in_audio_file out_audio_file
    """
    mkdir_by_file(output)
    await run_command([
            "ffmpeg",
            "-y",
            "-i",
            input,
            output
        ])
    return output

# 语音识别器
class AudioRecognizer:
    @classmethod
    async def recognize(self, audio_path: str) -> pysrt.SubRipFile: ...

# 语音识别生成字幕
async def audio_to_srt(audio_path: str, srt_path: str, recognizer: AudioRecognizer, delete_audio=False) -> str:
    try:
        srt_subs = await recognizer.recognize(audio_path)
        srt_subs.save(path=srt_path, encoding="utf-8")
    except:
        print(f"audio_to_srt failure: {audio_path}")
        raise
    if delete_audio:
        await remove_file(audio_path)
    print(f"audio_to_srt: {audio_path} -> {srt_path}")
    return srt_path
