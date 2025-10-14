import pysrt
from edge_srt_to_speech.__main__ import _main as audio_synthesis

from util import *

# 文本翻译器
class TextTranslator:
    @classmethod
    async def text_translate(text: str) -> str:...

# Ai 对话聊天器
class AiChatClient:
    @classmethod
    async def chat(self, input: str) -> str:...

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
