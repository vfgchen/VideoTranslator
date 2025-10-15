import asyncio
import argparse

from common_util import *
from audio import *
from subtitle import *

async def main():
    parser = argparse.ArgumentParser(description="*.res check")
    parser.add_argument("--subtitle_dir", help="subtitle directory", default="subtitles")
    parser.add_argument("--suffix", help="res filename suffix", default=".res")
    parser.add_argument("--topic", help="topic", default="Power Platform PL-200")
    args = parser.parse_args()

    subtitle_dir=args.subtitle_dir
    suffix=args.suffix
    topic=args.topic

    files = list_files(subtitle_dir, suffix)
    
    # 执行 *.res 检查
    results = await async_batch_exec(files, res_check)

    # 删除并重新生成 res_check.err
    res_check_err = path.join(subtitle_dir, "res_check.err")
    if path.exists(res_check_err):
        os.remove(res_check_err)
    err_infos = [err_info for match, res_name, err_info in results if not match]
    if len(err_infos) == 0:
        print(f"success, all is match ...")
        # 校验没有错误时删除所有 *.req
        await run_shell(f"rm {subtitle_dir}/*.req")
        return
    await write_lines(res_check_err, err_infos)

    # 存在错误时，恢复 *.req 文件
    txt_names = [with_ext(res_name, "txt") for match, res_name, err_info in results if not match]
    txt_paths = [project_resolve(subtitle_dir, txt_name) for txt_name in txt_names]
    await async_batch_exec(txt_paths, txt_to_req, topic)

if __name__ == "__main__":
    asyncio.run(main())
