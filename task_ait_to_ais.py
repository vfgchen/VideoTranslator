import asyncio
import argparse

from functools import partial

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    parser = argparse.ArgumentParser(description="*.ait to *.ais")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="req filename suffix", default=".ait")
    parser.add_argument("--ref_lang", help="req filename suffix", default="en")
    args = parser.parse_args()

    subtitle_dir = args.subtitle_dir
    suffix = args.suffix
    ref_lang = args.ref_lang

    # 先删除 ait_to_ais.err
    ait_to_ais_err_path = project_resolve(subtitle_dir, "ait_to_ais.err")
    await remove_file(ait_to_ais_err_path)

    # 生成 *.ais
    files = list_files(subtitle_dir, suffix)
    tuples = await async_batch_exec(files, ait_to_ais, ref_lang)
    
    # 有错重新生成 ait_to_ais.err
    errors = []
    for ais_path, errs in tuples:
        errors.extend(errs)
    if len(errors) > 0:
        await write_lines(ait_to_ais_err_path, errors)

if __name__ == "__main__":
    asyncio.run(main())
