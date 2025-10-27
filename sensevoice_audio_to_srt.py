import os
import glob
import argparse

import io
import emoji
import soundfile
import torch
from funasr import AutoModel
from funasr.utils.postprocess_utils import rich_transcription_postprocess

# 定义时间戳格式
def seconds_to_srttime(seconds):
    h, m  = divmod(seconds, 3600)
    m, s  = divmod(m, 60)
    s, ms = divmod(s, 1)
    return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(ms * 1000):03d}"

# 音频转字幕
def audio_to_srt(
        wav_file,
        srt_file,
        vad_model,
        asr_model,
        ):

    # 获取 vad 分段
    vad_res = vad_model.generate(input=wav_file, cache={})
    vad_segments = vad_res[0]["value"]

    if len(vad_segments) <= 0: return srt_file

    # 创建 srt 文件目录
    if not os.path.exists(os.path.dirname(srt_file)):
        os.makedirs(os.path.dirname(srt_file))

    # 加载原始音频数据
    audio_data, sample_rate = soundfile.read(wav_file)

    # 对每个分段语音识别生成字幕
    srt_items = []
    for vad_segment in vad_segments:
        # 截取音频片段
        start, end = vad_segment  # 获取开始和结束时间
        start_sample = int(start * sample_rate / 1000)  # 转换为样本数
        end_sample = int(end * sample_rate / 1000)  # 转换为样本数
        audio_segment = audio_data[start_sample:end_sample]

        # 语音转文字处理
        with io.BytesIO() as buffer:
            soundfile.write(buffer, audio_segment, sample_rate, format="WAV")
            buffer.seek(0)  # 重置缓冲区指针到开头
            asr_res = asr_model.generate(input=buffer, cache={})

        # 处理输出结果
        text = rich_transcription_postprocess(asr_res[0]["text"])
        text = emoji.replace_emoji(text, replace="")  # 去除表情符号
        text = text.strip()
        if text == "": continue
        srt_items.append(f"{len(srt_items)+1}\n{seconds_to_srttime(start / 1000)} --> {seconds_to_srttime(end / 1000)}\n{text}\n\n")

    # 字幕写入到文件
    with open(srt_file, "w", encoding="utf-8") as file:
        for srt_item in srt_items:
            file.write(srt_item)
    print(f"audio_to_srt: {srt_file}")
    return srt_file

def audios_to_srts(
    vad_model,
    asr_model,
    audio_dir   = "audios",
    srt_dir     = "subtitles",
    audio_type  = "wav",
    delete_wav  = "yes",
    lang        = "en",
    ):
    # 创建 srt 输出目录
    if not os.path.exists(srt_dir):
        os.makedirs(srt_dir)
    # 遍历 wav 或 mp3 文件，生成 srt
    for audio_file in glob.glob(os.path.join(audio_dir, f"**/*-{lang}.{audio_type}"), recursive=True):
        basename = os.path.basename(audio_file).split("-")[0]
        srt_file = f"{srt_dir}/{basename}-{lang}.srt"
        audio_to_srt(
            wav_file=audio_file,
            srt_file=srt_file,
            vad_model=vad_model,
            asr_model=asr_model,
        )
        if delete_wav.lower() == "yes":
            os.remove(audio_file)

# 加载模型
def load_models(
        model_dir="./models",
        lang="en",
        vad_model_dir="iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        asr_model_dir="iic/SenseVoiceSmall"
    ):
    # 模型路径
    vad_model_path = os.path.join(model_dir, vad_model_dir)
    asr_model_path = os.path.join(model_dir, asr_model_dir)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"use device: {device}")

    # 加载VAD模型
    vad_model = AutoModel(
        model=vad_model_dir,
        model_path=vad_model_path,
        device=device,
        disable_update=True,
        max_single_segment_time=20000,  # 最大单个片段时长
        merge_length_s=10,  # 合并长度，单位为秒
        max_end_silence_time=500,  # 静音阈值，范围500ms～6000ms，默认值800ms。
    )

    # 加载SenseVoice模型
    asr_model = AutoModel(
        model=asr_model_dir,
        model_path=asr_model_path,
        device=device,
        disable_update=True,
        language=lang,
        use_itn=True,
        batch_size_s=60,
        merge_vad=True,  # 启用 VAD 断句
        ban_emo_unk=True,  # 禁用情感标签
    )
    return vad_model, asr_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="audio to srt")
    parser.add_argument("--audio_dir", help="audio dir", default="audios")
    parser.add_argument("--srt_dir", help="srt dir", default="subtitles")
    parser.add_argument("--audio_type", help="audio type", default="mp3")
    parser.add_argument("--delete_wav", help="delete wav: yes, y, true, no, n, false", default="no")
    parser.add_argument("--lang", help="lang", default="en")
    parser.add_argument("--model_dir", help="model dir", default="./models")
    args = parser.parse_args()  

    vad_model, asr_model = load_models(
        model_dir       = args.model_dir,
        lang            = args.lang,
        vad_model_dir   = "iic/speech_fsmn_vad_zh-cn-16k-common-pytorch",
        asr_model_dir   = "iic/SenseVoiceSmall"
    )

    audios_to_srts(
        vad_model       = vad_model,
        asr_model       = asr_model,
        audio_dir       = args.audio_dir,
        srt_dir         = args.srt_dir,
        audio_type      = args.audio_type,
        delete_wav      = args.delete_wav,
        lang            = args.lang,
    )
