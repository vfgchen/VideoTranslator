import io
import torch
import pysrt
import emoji
import soundfile

from os import path
from functools import partial
from common_util import *
from audio import AudioRecognizer
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

# SenseVoice 语音识别器
class SenseVoiceAudioRecognizer(AudioRecognizer):
    def __init__(self,
            model_dir      = model_dir,
            vad_model_dir  = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
            asr_model_dir  = "iic/SenseVoiceSmall",
            device         = "cuda" if torch.cuda.is_available() else "cpu",
            lang           = "en"
        ):
        """
        加载 SenseVoice 模型
        """
        print(f"SenseVoice: model_dir={model_dir}, vad_model: {vad_model_dir}, asr_model: {asr_model_dir}, device: {device}")
        self.model_dir     = model_dir
        self.vad_model_dir = vad_model_dir
        self.asr_model_dir = asr_model_dir
        self.device        = device

        # 模型路径
        vad_model_path = path.join(model_dir, vad_model_dir)
        asr_model_path = path.join(model_dir, asr_model_dir)

        # 加载VAD模型
        self.vad_model = AutoModel(
            model           = vad_model_dir,
            model_path      = vad_model_path,
            device          = device,
            disable_update  = True,

            max_single_segment_time = 20000,  # 最大单个片段时长
            merge_length_s          = 10,     # 合并长度，单位为秒
            max_end_silence_time    = 500,    # 静音阈值，范围500ms～6000ms，默认值800ms。
        )

        # 加载 SenseVoice 模型
        self.asr_model = AutoModel(
            model           = asr_model_dir,
            model_path      = asr_model_path,
            device          = device,
            disable_update  = True,
            language        = lang,
            use_itn         = True,
            batch_size_s    = 60,
            merge_vad       = True,  # 启用 VAD 断句
            ban_emo_unk     = True,  # 禁用情感标签
        )
    
    async def recognize(self, audio_path) -> pysrt.SubRipFile:
        """
        语言识别
        """
        # 获取 vad 分段，线程池中运行转录，避免阻塞事件循环
        vad_res = await run_in_eventloop(
            partial(self.vad_model.generate, cache={}),
            audio_path
        )

        vad_segments = vad_res[0]["value"]
        if len(vad_segments) == 0: return []

        # 加载原始音频数据
        audio_data, sample_rate = soundfile.read(audio_path)

        # 对每个分段语音识别生成字幕
        srt_subs = pysrt.SubRipFile()
        for vad_segment in vad_segments:
            # 截取音频片段
            start, end = vad_segment  # 获取开始和结束时间
            start_sample = int(start * sample_rate / 1000)  # 转换为样本数
            end_sample = int(end * sample_rate / 1000)  # 转换为样本数
            audio_segment = audio_data[start_sample : end_sample]

            # 语音转文字处理，线程池中运行转录，避免阻塞事件循环
            with io.BytesIO() as buffer:
                soundfile.write(buffer, audio_segment, sample_rate, format="WAV")
                buffer.seek(0)  # 重置缓冲区指针到开头
                asr_res = await run_in_eventloop(
                    partial(self.asr_model.generate, cache={}),
                    buffer,
                )

            # 处理输出结果
            text = rich_transcription_postprocess(asr_res[0]["text"])
            text = emoji.replace_emoji(text, replace="")  # 去除表情符号
            text = text.strip()
            if text == "": continue
            
            srt_subs.append(pysrt.SubRipItem(
                index   = len(srt_subs) + 1,
                start   = start,
                end     = end,
                text    = text,
            ))
        return srt_subs
