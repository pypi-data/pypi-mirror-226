import openai
import typing
from .llm_client import LLMClient, LLMClientOptions, LLMMetadata
from ...env import global_openai_api_key


class AzureOpenAILLMClient(LLMClient):
    def __init__(
        self, *, deployment_name: str, api_key: None | str = None, **kwargs
    ) -> None:
        # The default temperature is 0, which means no randomness.
        if "temperature" not in kwargs:
            kwargs["temperature"] = 0

        super().__init__(
            LLMClientOptions(
                provider_name="AZURE",
                model_name=deployment_name,
                model_config=kwargs,
            )
        )
        self.api_key = api_key
        self.api_type = "azure"

    async def _generate_impl(
        self, prompt: str
    ) -> typing.Tuple[str, LLMMetadata, LLMClientOptions]:
        response = await openai.ChatCompletion.acreate(
            deployment_id=self.options.model_name,
            messages=[{"role": "user", "content": prompt}],
            api_key=self.api_key or global_openai_api_key(),
            api_type=self.api_type,
            **self.options.model_config,
        )
        raw_text = response.choices[0].message.content
        metadata = LLMMetadata(
            token_usage={
                "total": response.usage.total_tokens,
                "prompt": response.usage.prompt_tokens,
                "generated": response.usage.completion_tokens,
            }
        )
        options = self.options.copy()
        options.model_name = response.model

        return raw_text, metadata, options


__all__ = ["AzureOpenAILLMClient"]
