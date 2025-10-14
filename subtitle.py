import os
import re
import pysrt
from typing import Tuple

from edge_srt_to_speech.__main__ import _main as audio_synthesis

from common_util import *
from openai_prompt import *
from openai_chatclient import *

api_key  = os.environ.get('OPENAI_API_KEY')
base_url = "https://api.siliconflow.cn/v1"
model    = "deepseek-ai/DeepSeek-V3.2-Exp"

# res 行的正则匹配
res_line_regex = re.compile(r"^(?P<seq>\d+)[\.\s]*(?P<text>.*)$")

# *.srt -> *.txt
async def srt_to_txt(srt_path) -> Tuple[str, str]:
    txt_path = with_ext(srt_path, "txt")
    lines = [
        f"{sub.index}. {sub.text}" for sub in pysrt.open(srt_path)
    ]
    await write_lines(txt_path, lines)
    print(f"srt_to_txt: {srt_path} -> {txt_path}")
    return txt_path, "\n".join(lines)

# *.txt -> *.req
async def txt_to_req(txt_path, topic="") -> Tuple[str, str]:
    # 构建提示文本
    text = await read_file(txt_path)
    chat_content = build_chat_content(text, topic)

    # 生成 *.req
    req_path = with_ext(txt_path, "req")
    await write_text(req_path, chat_content)

    print(f"txt_to_req: {txt_path} -> {req_path}")
    return req_path, chat_content

# *.req -> *.res
async def req_to_res(req_path, chat_client: AiChatClient, remove_req=True) -> str:
    # 读取 *.req
    chat_input = await read_file(req_path)

    # 发送 deepseek 翻译处理
    chat_output = await chat_client.chat(chat_input)

    # 生成 *.res
    res_path = with_ext(req_path, "res")
    await write_text(res_path, chat_output)
    if remove_req: os.remove(req_path)

    return res_path

# *.res check
async def res_check(res_path) -> Tuple[bool, str, str]:
    res_lines = [line.strip() for line in await read_lines(res_path) if res_line_regex.match(line)]

    # *-en.txt
    txt_path = with_ext(res_path, "txt")
    assert path.exists(txt_path)
    txt_lines = [line.strip() for line in await read_lines(txt_path) if len(line.strip()) > 0]

    # 校验行数
    txt_name = path.basename(txt_path)
    res_name = path.basename(res_path)
    len_res  = int(len(res_lines) / 2)
    len_txt  = len(txt_lines)
    if len_res != len_txt:
        return False, res_name, f"{res_name} : {len_res} : {len_txt} : {txt_name}"
    
    # 校验序号
    for index, res_line in enumerate(res_lines):
        txt_line = txt_lines[index % len_txt]
        res_seq = res_line_regex.match(res_line)["seq"]
        txt_seq = res_line_regex.match(txt_line)["seq"]
        if int(res_seq) != int(txt_seq):
            return False, res_name, f"{res_name} : {res_line} : {txt_line}"
    return True, res_name, "success"

# *.res -> *-en.ait *-zh.ait
async def res_to_ait(res_path) -> Tuple[str, str]:
    # 读取 res 文件中有效行
    lines = await read_lines(res_path)
    lines = [
        line.strip() for line in lines if res_line_regex.match(line)
    ]

    # 进行英文和中文拆分
    en_lines = []
    zh_lines = []
    length = len(lines)
    for index, line in enumerate(lines):
        if index < length / 2:
            en_lines.append(line)
        else:
            zh_lines.append(line)
    try:
        assert len(en_lines) == len(zh_lines)
    except:
        print(f"res_to_ait: {res_path} {len(en_lines)} : {len(zh_lines)}")
        raise

    # 生成 *-en.ait *-zh.ait
    en_ait_path = with_lang_ext(res_path, "en", "ait")
    zh_ait_path = with_lang_ext(res_path, "zh", "ait")
    await write_lines(en_ait_path, en_lines)
    await write_lines(zh_ait_path, zh_lines)

    return en_ait_path, zh_ait_path

# *.ait 文件和 *.txt 文件行数比对校验
async def ait_check(ait_path, lang="en") -> Tuple[bool, str]:
    # 读取 *-{lang}.ait 文件的行
    ait_lines = await read_lines(ait_path)
    ait_lines = [line.strip() for line in ait_lines if line.strip()]

    # 读取 *-{lang}.txt 文件的行
    txt_path = with_lang_ext(ait_path, lang, "txt")
    assert path.exists(txt_path)
    txt_lines = await read_lines(txt_path)
    txt_lines = [line.strip() for line in txt_lines if line.strip()]

    len_ait = len(ait_lines)
    len_txt = len(txt_lines)
    ait_name = path.basename(ait_path)
    txt_name = path.basename(txt_path)
    report = f"{ait_name} : {len_ait:03d} : {len_txt:03d} : {txt_name}"

    # 判断行数是否匹配
    if (len_ait != len_txt): print(report)
    return len_ait == len_txt, report

# *.ait -> *.ais 字幕
async def ait_to_ais(ait_path, ref_srt_lang="en") -> Tuple[str, list]:
    # 读取 *.ait
    ait_lines = await read_lines(ait_path)
    ait_lines = [line.strip() for line in ait_lines if res_line_regex.match(line)]

    # 读取参考字幕
    ref_srt = with_lang_ext(ait_path, ref_srt_lang, "srt")
    assert path.exists(ref_srt)
    ref_subs = pysrt.open(ref_srt)
    
    # 断言 *.ait 和 *.srt 条目数相等
    assert len(ait_lines) == len(ref_subs)
    ait_name = path.basename(ait_path)

    # 错误和警告收集
    errors = []

    # ais 字幕
    ais_subs = pysrt.SubRipFile()
    # 生成 *.ais 字幕，校验行号并替换字幕文本
    for index, sub in enumerate(ref_subs):
        ait_line = ait_lines[index]
        # 读取 *.ait 行，校验行号是否匹配，替换字幕文本
        group = res_line_regex.match(ait_line)
        try:
            assert sub.index == int(group["seq"])
        except:
            errors.append(f"error: {ait_name}, {ait_line}")
        sub.text = group["text"].strip()
        if sub.text:
            ais_subs.append(sub)
        elif len(ais_subs) > 0:
            # sub 文本为空时，将此行字幕合并到上一行
            ais_subs[-1].end = sub.end
            errors.append(f"warn : {ait_name}, {ait_line}")
    ais_path = with_ext(ait_path, "ais")
    ais_subs.save(ais_path, encoding="utf-8")

    print(f"ait_to_ais: {ait_path} -> {ais_path}")
    return ais_path, errors

# *.srt , *.ais -> *.mp3 语音合成
async def srt_to_mp3(srt_path, mp3_path, voice="zh-CN-XiaoxiaoNeural", delete_ais=False) -> str:
    mkdir_by_file(mp3_path)
    # 字幕语音合成
    await audio_synthesis(
        srt_data = pysrt.open(srt_path),
        voice = voice,
        out_file = mp3_path,
        rate = "+0%",
        volume = "+0%",
        batch_size = 50,
        enhanced_srt = False,
    )
    if delete_ais: await remove_file(srt_path)
    return mp3_path
