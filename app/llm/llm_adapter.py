import json

from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.utils.error import BusinessException


# Adapter for LLMs. Allow faster replacement of LLM Backend.
class LLMAdapter:

    def __init__(self):
        self.client = AsyncOpenAI()

    async def do_text_classification(self, systemPrompt: str, userPrompt: str) -> dict:

        try:
            result: ChatCompletion = await self.client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": systemPrompt},
                    {"role": "user", "content": userPrompt},
                ],
                max_tokens=1024,
                temperature=0.2,
                top_p=0.1,
            )
            content = result.choices[0].message.content

            if type(content) is not str:
                raise BusinessException(
                    502, "LLM Result is not valid: {content}".format(content), None
                )

            return json.loads(str(content))
        except Exception as err:
            raise BusinessException(502, "Calling the LLM caused an exception", err)
