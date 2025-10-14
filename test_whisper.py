import asyncio

from util import *
from audio import *
from subtitle import *

from openai_whisper import *
from openai_deepseek import *

async def main():
    audio_path  = f"D:/output/005-en.mp3"
    srt_path    = f"D:/output/005-en.srt"
    en_ait_path = f"D:/output/005-en.ait"
    zh_ait_path = f"D:/output/005-zh.ait"
    topic       = "Power Platform PL-100"

    # audio_recognizer = WhisperAudioRecognizer()
    # audio_processor = AudioProcessor(recognizer=audio_recognizer)
    # await audio_processor.audio_to_srt(audio_path, srt_path)

    txt_path, txt_content = await srt_to_txt(srt_path)
    txt_translator = DeepseekTxtTranslator(
        api_key="sk-gzamafbtljbkvojurobnfzvzinrbpgljavbuuhggofhfjcdc",
        base_url="https://api.siliconflow.cn/v1",
        model="deepseek-ai/DeepSeek-V3.2-Exp",
        topic="Power Platform PL-100",
        )
    zh_ait_path, zh_ait_txt = await txt_translator.txt_to_ait(txt_path)

    is_match, diff_info = await ait_check(zh_ait_path, "en")
    print(f"{is_match} : {diff_info}")

    en_ais_path, en_errors = await ait_to_ais(en_ait_path, ref_srt_lang="en")
    zh_ais_path, zh_errors = await ait_to_ais(zh_ait_path, ref_srt_lang="en")


if __name__ == "__main__":
    asyncio.run(main())
