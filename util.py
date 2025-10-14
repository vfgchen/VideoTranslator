import os
import glob
import asyncio
from os import path
from typing import List, Tuple

# 定义工程下的各种目录路径
project_dir  = path.dirname(__file__)
model_dir    = path.join(project_dir, "models")
video_dir    = path.join(project_dir, "videos")
audio_dir    = path.join(project_dir, "audios")
subtitle_dir = path.join(project_dir, "subtitles")

def project_resolve(*item):
    return path.join(project_dir, *item)

def mkdir_by_file(file_path: str):
    if not path.exists(path.dirname(file_path)):
        os.makedirs(path.dirname(file_path))

def with_ext(file_path, ext):
    return f"{path.splitext(file_path)[0]}.{ext}"

def with_lang_ext(file_path, lang, ext):
    basename = file_path.split("-")[0]
    return f"{basename}-{lang}.{ext}"

def seconds_to_srttime(seconds):
    """
    srt 时间格式: 00:00:00,000
    """
    seconds = float(seconds)
    h, m  = divmod(seconds, 3600)
    m, s  = divmod(m, 60)
    s, ms = divmod(s, 1)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(ms * 1000):03d}"

def batch_generator(data, batch_size):
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

async def run_in_eventloop(func, *args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)

async def write_text(file_path, text):
    with open(file_path, "w", encoding="utf-8") as file:
        await run_in_eventloop(file.write, text)

async def write_lines(file_path, lines):
    text="\n".join(lines)
    await write_text(file_path,  f"{text}\n")

async def read_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return await run_in_eventloop(file.read)

async def read_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return await run_in_eventloop(file.readlines)

async def remove_file(file_path):
    if path.exists(file_path):
        await run_in_eventloop(os.remove, file_path)

async def run_command(command: List[str]) -> Tuple[bool, str, str]:
    """执行命令并返回结果"""
    try:
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        success = process.returncode == 0
        return success, stdout.decode(), stderr.decode()
    except Exception as e:
        return False, "", str(e)

async def run_shell(shell_command: str) -> Tuple[bool, str, str]:
    """执行shell命令"""
    try:
        process = await asyncio.create_subprocess_shell(
            shell_command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        success = process.returncode == 0
        return success, stdout.decode(), stderr.decode()
    except Exception as e:
        return False, "", str(e)

def list_files(dir, suffix) -> List[str]:
    return glob.glob(path.join(dir, f"**/*{suffix}"), recursive=True)

def batch_exec(items, func, *args):
    return [func(item, *args) for item in items]

async def async_batch_exec(items, async_func, *args, batch_size=10):
    results = []
    for batch in batch_generator(items, batch_size):
        print(f"exec batch [{async_func.__name__}]:\n\t" + "\n\t".join(batch))
        tasks = [async_func(item, *args) for item in batch]
        results.extend(await asyncio.gather(*tasks))
    return results
