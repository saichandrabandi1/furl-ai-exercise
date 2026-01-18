# Furl AI Exercise

Build a small AI-assisted service that returns the release details for a piece of software on a specific OS.

## Goal

Implement the scaffold so the system accepts a software query (vendor, software name, OS details) and returns a structure containing:

- `release_notes_url`
- `download_url`
- `version`

## Scenarios

This exercise includes three test scenarios for Mozilla Firefox:

- Windows 11 (x86_64) latest release (non-pinned; prints output; structure-only assertions)
- Windows 10 (x86_64) pinned to version 147.0.1
- Windows 7 (x86_64) pinned to the 115 ESR release

Each scenario is isolated in its own test file so more scenarios can be added later.
Pinned versions for the Windows 10 test live in `tests/scenario_data.py` for easy updates.

## Project layout

- `src/furl_ai_exercise/models.py`: data models
- `src/furl_ai_exercise/service.py`: core logic (scaffold)
- `tests/test_firefox_windows11.py`: scenario test
- `tests/test_firefox_windows10_pinned.py`: scenario test
- `tests/test_firefox_windows7_esr.py`: scenario test

## What you need to implement

Fill in the TODO in `src/furl_ai_exercise/service.py` inside `run_release_graph`:

- Build and execute the LangGraph graph using a LangChain-compatible model
- Parse the JSON response into `ReleaseInfo`

The goal is for the test to pass with the provided fake LLM response.
You may update the prompt and graph structure as you see fit. The scaffolding provides
helpers (`build_prompt`, `build_release_graph`) for convenience, but they are not mandatory.

Implementation expectations for `run_release_graph`:

- Build or reuse a `StateGraph` that accepts the `ReleaseState` keys: `query` and `response`
- Invoke the graph with the incoming `SoftwareQuery` and capture the model output string
- Parse the JSON-only model response into `ReleaseInfo` and return it
- Keep the behavior compatible with a fake `RunnableLambda` that returns a raw string

Avoid modifying tests or the data models; the exercise is intentionally scoped to the graph execution and JSON parsing.

## Input / output shape

Input (`SoftwareQuery`):

- `vendor` (str)
- `software` (str)
- `os_name` (str)
- `os_version` (str)
- `cpu_arch` (str)
- `version` (str, optional; omit for latest lookups, set for pinned lookups)

Output (`ReleaseInfo`):

- `release_notes_url` (str)
- `download_url` (str)
- `version` (str)

Graph state (`ReleaseState`):

- `query` (`SoftwareQuery`)
- `response` (str)

## LLM configuration

This project uses LangChain + LangGraph. Bring any LangChain-compatible chat model or runnable.

Example (install provider package yourself):

```python
from langchain_openai import ChatOpenAI
from furl_ai_exercise.service import run_release_graph

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
result = run_release_graph(query, llm)
```

Provide your provider's API key as required (e.g. `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`).
Refer to the model provider docs for exact environment variables.

## Setup

1. `cd furl-ai-exercise`
2. `poetry install`
3. `poetry run pytest`

## Notes

- The test uses a fake runnable, so it runs without any real API calls.
- Keep outputs strictly JSON when calling the model.
- Python version is defined in `pyproject.toml` (`^3.12`).
- Agentic coding tools are allowed (Codex, Claude Code, Cursor, etc.) as long as you submit the full chat log with your assignment.
