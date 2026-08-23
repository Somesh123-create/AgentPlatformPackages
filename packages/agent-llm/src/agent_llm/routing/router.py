from agent_llm.providers.base import LLMProvider


class ProviderRouter:

    def __init__(
            self,
            providers: dict[str, LLMProvider],
        ):
        self.providers = providers


    def get_provider(
            self,
            provider_name: str,
        ) -> LLMProvider:

        provider = self.providers.get(
            provider_name
        )

        if provider is None:
            raise ValueError(
                f"Unsupported LLM provider: "
                f"{provider_name}"
            )

        return provider