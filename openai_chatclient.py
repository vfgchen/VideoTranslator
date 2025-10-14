import os
from openai import AsyncOpenAI

api_key  = os.environ.get('OPENAI_API_KEY')
base_url = "https://api.siliconflow.cn/v1"
model    = "deepseek-ai/DeepSeek-V3.2-Exp"

# Ai 对话聊天器
class AiChatClient:
    @classmethod
    async def chat(self, input: str) -> str:...

# Deepseek 文本翻译器
class OpenAiChatClient(AiChatClient):
    def __init__(self, topic, model=model, api_key=api_key, base_url=base_url):
        self.topic = topic
        self.model = model
        self.chat_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
    
    async def chat(self, input: str) -> str:
        # AI 对话
        print(f"chat send: {input}")
        response = await self.chat_client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"{input}"},
            ],
            stream=False
        )
        output = response.choices[0].message.content
        print(f"chat receive: {output}")
        return output
