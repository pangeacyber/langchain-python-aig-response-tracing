from __future__ import annotations

from typing import Any, override

import click
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

from langchain_aig_response_tracing.tracers import PangeaAIGuardCallbackHandler


class SecretStrParamType(click.ParamType):
    name = "secret"

    @override
    def convert(self, value: Any, param: click.Parameter | None = None, ctx: click.Context | None = None) -> SecretStr:
        if isinstance(value, SecretStr):
            return value

        return SecretStr(value)


SECRET_STR = SecretStrParamType()


@click.command()
@click.option("--model", default="gpt-4o-mini", show_default=True, required=True, help="OpenAI model.")
@click.option(
    "--ai-guard-token",
    envvar="PANGEA_AI_GUARD_TOKEN",
    type=SECRET_STR,
    required=True,
    help="Pangea AI Guard API token. May also be set via the `PANGEA_AI_GUARD_TOKEN` environment variable.",
)
@click.option(
    "--ai-guard-config-id",
    help="Pangea AI Guard configuration ID.",
)
@click.option(
    "--pangea-domain",
    envvar="PANGEA_DOMAIN",
    default="aws.us.pangea.cloud",
    show_default=True,
    required=True,
    help="Pangea API domain. May also be set via the `PANGEA_DOMAIN` environment variable.",
)
@click.option(
    "--openai-api-key",
    envvar="OPENAI_API_KEY",
    type=SECRET_STR,
    required=True,
    help="OpenAI API key. May also be set via the `OPENAI_API_KEY` environment variable.",
)
@click.argument("prompt")
def main(
    *,
    prompt: str,
    ai_guard_token: SecretStr,
    ai_guard_config_id: str | None = None,
    pangea_domain: str,
    model: str,
    openai_api_key: SecretStr,
) -> None:
    ai_guard_callback = PangeaAIGuardCallbackHandler(
        token=ai_guard_token, domain=pangea_domain, config_id=ai_guard_config_id
    )
    chain = (
        ChatPromptTemplate.from_messages([("user", "{input}")])
        | ChatOpenAI(model=model, api_key=openai_api_key, callbacks=[ai_guard_callback])
        | StrOutputParser()
    )
    click.echo(chain.invoke({"input": prompt}))


if __name__ == "__main__":
    main()
