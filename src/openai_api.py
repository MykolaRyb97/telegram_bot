
from settings.utils import get_logger
from settings.config import config
from openai import AsyncOpenAI, OpenAIError

logger = get_logger(__name__)

class OpenAIClient:
    def __init__(self, openai_api_key: str, model: str, temperature: float):
        self._client = AsyncOpenAI(api_key=openai_api_key)
        self._model = model
        self._temperature = temperature

    async def take_task(
            self,
            prompt: str | list[dict],
            system_prompt: str = 'You are a helpful assistant'
    ) -> str | None:
        try:
            if isinstance(prompt, list):  # Якщо це вже список повідомлень
                messages = prompt
            else:
                messages = [
                    {'role': 'system', 'content': system_prompt},
                    {'role': 'user', 'content': prompt}
                ]

            response = await self._client.chat.completions.create(
                model=self._model,
                messages=messages,
                temperature=self._temperature
            )
            return response.choices[0].message.content
        except OpenAIError as e:
            logger.error(f'OpenAI Error: {e}')
            raise

openai_client = OpenAIClient(
    openai_api_key=config.OPENAI_API_KEY,
    model=config.openai_model,
    temperature=config.openai_model_temperature
)

async def get_chatgpt_response(prompt: str | list[dict], system_prompt: str = 'You are a helpful assistant') -> str:
    return await openai_client.take_task(prompt, system_prompt)