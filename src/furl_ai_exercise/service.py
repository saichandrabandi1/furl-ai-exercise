from __future__ import annotations

import json
from typing import TypedDict

from langchain_core.runnables import Runnable
from langgraph.graph import END, StateGraph

from furl_ai_exercise.models import ReleaseInfo, SoftwareQuery


def build_prompt(query: SoftwareQuery) -> str:
    prompt = (
        "You are a release intelligence assistant. "
        "Given vendor, software, OS, OS version, and CPU architecture, "
        "respond with ONLY JSON containing: release_notes_url, download_url, version.\n\n"
        f"Vendor: {query.vendor}\n"
        f"Software: {query.software}\n"
        f"OS: {query.os_name}\n"
        f"OS Version: {query.os_version}\n"
        f"CPU Architecture: {query.cpu_arch}\n"
    )
    if query.version:
        prompt += f"Requested Version: {query.version}\n"
    return prompt


def parse_release_info(raw: str) -> ReleaseInfo:
    data = json.loads(raw)
    return ReleaseInfo(
        release_notes_url=data["release_notes_url"],
        download_url=data["download_url"],
        version=data["version"],
    )


class ReleaseState(TypedDict):
    query: SoftwareQuery
    response: str


def _call_model(state: ReleaseState, llm: Runnable) -> ReleaseState:
    prompt = build_prompt(state["query"])
    raw = llm.invoke(prompt)
    content = raw.content if hasattr(raw, "content") else raw
    return {"query": state["query"], "response": content}


def build_release_graph(llm: Runnable) -> Runnable:
    graph = StateGraph(ReleaseState)
    graph.add_node("call_model", lambda state: _call_model(state, llm))
    graph.set_entry_point("call_model")
    graph.add_edge("call_model", END)
    return graph.compile()


def run_release_graph(query: SoftwareQuery, llm: Runnable) -> ReleaseInfo:
    """
    Execute the release graph and return the parsed release info.
    """
    # TODO: build the graph, invoke it with the query, and parse the response.
    raise NotImplementedError("Implement run_release_graph in service.py")
