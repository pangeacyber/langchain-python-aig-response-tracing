from __future__ import annotations

import itertools
from typing import Any, override
from uuid import UUID

from langchain_core.outputs import ChatGeneration, LLMResult
from langchain_core.tracers.base import BaseTracer
from langchain_core.tracers.schemas import Run
from pangea import PangeaConfig
from pangea.services import AIGuard
from pydantic import SecretStr

__all__ = ["PangeaAIGuardCallbackHandler"]


class PangeaAIGuardCallbackHandler(BaseTracer):
    """
    Pangea AI guard tracer.
    """

    _client: AIGuard

    def __init__(
        self,
        *,
        token: SecretStr,
        config_id: str | None = None,
        domain: str = "aws.us.pangea.cloud",
        log_missing_parent: bool = False,
        **kwargs: Any,
    ) -> None:
        """
        Args:
            token: Pangea AI Guard API token.
            config_id: Pangea AI Guard configuration ID.
            domain: Pangea API domain.
        """

        super().__init__(**kwargs)
        self.log_missing_parent = log_missing_parent
        self._client = AIGuard(token=token.get_secret_value(), config=PangeaConfig(domain=domain), config_id=config_id)

    @override
    def _persist_run(self, run: Run) -> None:
        pass

    @override
    def on_llm_end(self, response: LLMResult, *, run_id: UUID, **kwargs: Any) -> Run:
        generations = itertools.chain.from_iterable(response.generations)
        chat_generations = [x for x in generations if isinstance(x, ChatGeneration)]

        for x in chat_generations:
            guarded = self._client.guard_text(x.text, recipe="pangea_llm_response_guard")
            assert guarded.result

            if guarded.result.redacted_prompt:
                x.message.content = guarded.result.redacted_prompt
                ChatGeneration.model_validate(x, strict=True)

        return super().on_llm_end(response, run_id=run_id, **kwargs)
