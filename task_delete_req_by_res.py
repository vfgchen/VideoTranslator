import os
import asyncio

from util import *
from audio import *
from subtitle import *

from openai_deepseek import *

def delete_req_by_res(res_path):
    os.remove(with_ext(res_path, "req"))

def main():
    files = list_files(subtitle_dir, ".res")
    batch_exec(files, delete_req_by_res)

if __name__ == "__main__":
    main()
