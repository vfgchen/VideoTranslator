import whisper
import torch
import pysrt
from functools import partial

from common_util import *
from audio import AudioRecognizer

# Whisper 语音识别器
class WhisperAudioRecognizer(AudioRecognizer):
    def __init__(self,
            model_name = "base.en",
            model_dir  = model_dir,
            device     = "cuda" if torch.cuda.is_available() else "cpu"
        ):
        """
        加载 whisper 模型
        """
        print(f"whisper: model_name={model_name}, model_dir: {model_dir}, device: {device}")
        self.model_name = model_name
        self.model_dir  = model_dir
        self.device     = device
        self.asr_model  = whisper.load_model(
            name=model_name,
            download_root=model_dir,
            device=device,
        )
    
    async def recognize(self, audio_path) -> pysrt.SubRipFile:
        """
        语言识别
        """
        # 线程池中运行转录，避免阻塞事件循环
        result = await run_in_eventloop(
            partial(self.asr_model.transcribe, verbose=True),
            audio_path,
        )

        # 转成 srt 文件
        srt_subs = pysrt.SubRipFile()
        for segment in result["segments"]:
            text  = segment["text"].strip()
            if len(text) == 0: continue
            srt_subs.append(pysrt.SubRipItem(
                index = len(srt_subs) + 1,
                start = seconds_to_srttime(segment["start"]),
                end   = seconds_to_srttime(segment["end"]),
                text  = text,
            ))
        return srt_subs
