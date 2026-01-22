import json
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from furl_ai_exercise.models import SoftwareQuery, ReleaseInfo


# 1. Build the prompt for the model
def build_prompt(query: SoftwareQuery) -> str:
    """
    Build a structured prompt for the LLM.
    Ensures the model returns ONLY valid JSON with required keys.
    """
    prompt = (
        "You are a release intelligence assistant.\n"
        "Given vendor, software, OS, OS version, and CPU architecture,\n"
        "respond with ONLY JSON containing: release_notes_url, download_url, and version.\n\n"
        f"Vendor: {query.vendor}\n"
        f"Software: {query.software}\n"
        f"OS: {query.os_name}\n"
        f"OS Version: {query.os_version}\n"
        f"CPU Architecture: {query.cpu_arch}\n"
    )

    # Include pinned version if provided
    if query.version:
        prompt += f"\nPinned Version: {query.version}"

    # Always end with strict JSON-only instruction
    prompt += (
        "\n\nReturn ONLY valid JSON with keys: "
        "release_notes_url, download_url, and version."
    )
    return prompt.strip()


# 2. Parse the model's response into structured data
def parse_release_info(raw: str) -> ReleaseInfo:
    """
    Parse the model's JSON response into a ReleaseInfo object.
    Handles markdown formatting and ensures valid JSON.
    """
    raw = raw.strip()

    # Remove markdown code fences if present
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()
        raw = raw.strip("`").strip()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from model: {raw}") from e

    return ReleaseInfo(
        release_notes_url=data.get("release_notes_url", ""),
        download_url=data.get("download_url", ""),
        version=data.get("version", "")
    )


# 3. Define the LangGraph state
class ReleaseState(TypedDict):
    query: SoftwareQuery
    response: str


# 4. Node: Call the model
def _call_model(state: ReleaseState, llm: Runnable) -> ReleaseState:
    """
    Node that calls the LLM with the built prompt and returns the response.
    """
    prompt = build_prompt(state["query"])
    raw = llm.invoke(prompt)
    content = raw.content if hasattr(raw, "content") else raw
    return {"query": state["query"], "response": content}


# 5. Node: Parse the model response
def _parse_response(state: ReleaseState) -> ReleaseState:
    """
    Node that parses the model's response into structured JSON.
    """
    response = str(state["response"]).strip()
    if response.startswith("```"):
        response = response.strip("`").replace("json", "", 1).strip()

    parsed = parse_release_info(response)
    return {"query": state["query"], "response": parsed}


# 6. Build the LangGraph workflow
def build_release_graph(llm: Runnable) -> Runnable:
    """
    Build and compile the LangGraph workflow with defined nodes and edges.
    """
    graph = StateGraph(ReleaseState)

    # Add nodes
    graph.add_node("call_model", lambda state: _call_model(state, llm))
    graph.add_node("parse_response", _parse_response)

    # Define flow
    graph.set_entry_point("call_model")
    graph.add_edge("call_model", "parse_response")
    graph.add_edge("parse_response", END)

    # Compile the graph
    return graph.compile()


# 7. Run the graph and return structured ReleaseInfo
def run_release_graph(query: SoftwareQuery, llm: Runnable) -> ReleaseInfo:
    """
    Execute the LangGraph workflow and return the final structured result.
    """
    graph = build_release_graph(llm)
    final_state = graph.invoke({"query": query})

    # The final state's response is already a ReleaseInfo object
    result = final_state["response"]
    if isinstance(result, ReleaseInfo):
        return result

    # Fallback: parse if still string
    return parse_release_info(str(result))
