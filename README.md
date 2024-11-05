# AI Guard Response Tracing for LangChain in Python

An example Python app demonstrating how to integrate Pangea's [AI Guard][]
service into a LangChain app to monitor and sanitize LLM generations.

## Prerequisites

- Python v3.12 or greater.
- pip v24.2 or [uv][] v0.4.29.
- A [Pangea account][Pangea signup] with AI Guard enabled.
- An [OpenAI API key][OpenAI API keys].

## Setup

```shell
git clone https://github.com/pangeacyber/langchain-python-aig-response-tracing.git
cd langchain-python-aig-response-tracing
```

If using pip:

```shell
python -m venv .venv
source .venv/bin/activate
pip install .
```

Or, if using uv:

```shell
uv sync
source .venv/bin/activate
```

The sample can then be executed with:

```shell
python -m langchain_aig_response_tracing "What is MFA?"
```

## Usage

```
Usage: python -m langchain_aig_response_tracing [OPTIONS] PROMPT

Options:
  --model TEXT               OpenAI model.  [default: gpt-4o-mini; required]
  --ai-guard-token SECRET    Pangea AI Guard API token. May also be set via
                             the `PANGEA_AI_GUARD_TOKEN` environment variable.
                             [required]
  --ai-guard-config-id TEXT  Pangea AI Guard configuration ID.
  --pangea-domain TEXT       Pangea API domain. May also be set via the
                             `PANGEA_DOMAIN` environment variable.  [default:
                             aws.us.pangea.cloud; required]
  --openai-api-key SECRET    OpenAI API key. May also be set via the
                             `OPENAI_API_KEY` environment variable.
                             [required]
  --help                     Show this message and exit.
```

### Example Input/Output

AI Guard will protect against leaking credentials like Pangea API tokens. The
easiest way to demonstrate this would be to have the LLM repeat a given (fake)
API token:

```shell
python -m langchain_aig_response_tracing "Echo 'pts_testtesttesttesttesttesttesttest' back."
```

The output after AI Guard is:

```
************************************
```

Audit logs can be viewed at the [Secure Audit Log Viewer][].

[AI Guard]: https://pangea.cloud/docs/ai-guard/
[Secure Audit Log Viewer]: https://console.pangea.cloud/service/audit/logs
[Pangea signup]: https://pangea.cloud/signup
[OpenAI API keys]: https://platform.openai.com/api-keys
[uv]: https://docs.astral.sh/uv/
