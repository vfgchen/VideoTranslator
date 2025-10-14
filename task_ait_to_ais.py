import asyncio

from functools import partial

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

async def main():
    # 先删除 ait_to_ais.err
    ait_to_ais_err_path = project_resolve(subtitle_dir, "ait_to_ais.err")
    await remove_file(ait_to_ais_err_path)

    # 生成 *.ais
    files = list_files(subtitle_dir, ".ait")
    tuples = await async_batch_exec(files, ait_to_ais, "en")
    
    # 有错重新生成 ait_to_ais.err
    errors = []
    for ais_path, errs in tuples:
        errors.extend(errs)
    if len(errors) > 0:
        await write_lines(ait_to_ais_err_path, errors)


if __name__ == "__main__":
    asyncio.run(main())
