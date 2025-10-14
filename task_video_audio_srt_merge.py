import asyncio
import argparse

from os import path

from common_util import *
from video import *

async def namp4_mp3_srts_merge(file_path, mp4_dir, mp3_dir, srt_dir, srt_type="ais"):
    basename = path.basename(file_path).split("-")[0]
    namp4_path = path.join(mp4_dir, f"{basename}-na.mp4")
    zhmp3_path = path.join(mp3_dir, f"{basename}-zh.mp3")
    zhsrt_path = path.join(srt_dir, f"{basename}-zh.{srt_type}")
    ensrt_path = path.join(srt_dir, f"{basename}-en.{srt_type}")
    zhmp4_path = path.join(mp4_dir, f"{basename}-zh.mp4")

    assert path.exists(namp4_path)
    assert path.exists(zhmp3_path)
    assert path.exists(ensrt_path)
    assert path.exists(zhsrt_path)
    return await video_audio_srts_merge(
        na_video=namp4_path,
        zh_audio=zhmp3_path,
        zh_srt=zhsrt_path,
        en_srt=ensrt_path,
        zh_video=zhmp4_path)    

async def main():
    parser = argparse.ArgumentParser(description="video to audio")
    parser.add_argument("--root_dir", help="root directory", default=".")
    parser.add_argument("--suffix", help="filename suffix", default="na.mp4")
    parser.add_argument("--mp4_dirname", help="video directory name", default="videos")
    parser.add_argument("--mp3_dirname", help="audio directory name", default="audios")
    parser.add_argument("--srt_dirname", help="subtitle directory name", default="subtitles")
    parser.add_argument("--srt_type", help="srt type", default="ais")
    args = parser.parse_args()

    root_dir = args.root_dir
    suffix   = args.suffix
    root_dir = args.root_dir
    suffix   = args.suffix
    mp4_dir  = path.join(root_dir, args.mp4_dirname)
    mp3_dir  = path.join(root_dir, args.mp3_dirname)
    srt_dir  = path.join(root_dir, args.srt_dirname)
    srt_type = args.srt_type

    files = list_files(root_dir, suffix)
    await async_batch_exec(files, namp4_mp3_srts_merge, mp4_dir, mp3_dir, srt_dir, srt_type)

if __name__ == "__main__":
    asyncio.run(main())
