from os import path

from util import *

async def video_to_na_mp4(input: str, output: str) -> str:
    """
    提取无声视频
    ffmpeg -y -i "demo-en.mp4" -an -vcodec copy "demo-na.mp4"
    """
    mkdir_by_file(output)
    await run_command([
            "ffmpeg",
            "-y",
            "-i",
            input,
            "-an",
            "-vcodec",
            "copy",
            output
        ])
    return output

async def video_to_wav(input: str, output: str) -> str:
    """
    提取wav音频并以16khz输出
    ffmpeg -y -i "demo.mp4" -acodec pcm_s16le -ar 16000 "demo-en.wav"
    """
    mkdir_by_file(output)
    await run_command([
            "ffmpeg",
            "-y",
            "-i",
            input,
            "-acodec",
            "pcm_s16le",
            "-ar",
            "16000",
            output
        ])
    return output
    
async def video_to_mp3(input: str, output: str) -> str:
    """
    提取mp3音频并以16khz输出
    ffmpeg -y -i "demo.mp4" -acodec libmp3lame -ar 16000 "demo-en.mp3"
    """
    mkdir_by_file(output)
    await run_command([
            "ffmpeg",
            "-y",
            "-i",
            input,
            "-acodec",
            "libmp3lame",
            "-ar",
            "16000",
            output
        ])
    return output

async def video_audio_srts_merge(
        na_video: str,
        zh_audio: str,
        zh_srt: str,
        en_srt: str,
        zh_video: str,
    ) -> str:
    assert path.exists(na_video)
    assert path.exists(zh_audio)
    assert path.exists(zh_srt)
    assert path.exists(en_srt)

    """
    # 视频音频字幕合并
    ffmpeg -y
        -i "demo-na.mp4"
        -i "demo-zh.mp3"
        -i "demo-zh.srt"
        -i "demo-en.srt"
        -map 0 -dn -ignore_unknown -map -0:s
        -map 1 -dn -ignore_unknown -map -1:s
        -map 2:0 -metadata:s:s:0 "language=zho"
        -map 3:0 -metadata:s:s:1 "language=eng"
        -vcodec copy
        -acodec copy
        -strict experimental
        -c:s mov_text "output.mp4"
    """
    mkdir_by_file(zh_video)
    await run_command([
            "ffmpeg",
            "-y",
            "-i", na_video,
            "-i", zh_audio,
            "-i", zh_srt,
            "-i", en_srt,
            "-map", "0", "-dn", "-ignore_unknown", "-map", "-0:s",
            "-map", "1", "-dn", "-ignore_unknown", "-map", "-1:s",
            "-map", "2:0", "-metadata:s:s:0", "language=zho",
            "-map", "3:0", "-metadata:s:s:1", "language=eng",
            "-vcodec", "copy",
            "-acodec", "copy",
            "-strict", "experimental",
            "-c:s", "mov_text",
            zh_video
        ])
    return zh_video
