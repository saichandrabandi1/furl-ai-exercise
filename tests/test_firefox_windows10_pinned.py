from langchain_core.runnables import RunnableLambda

from furl_ai_exercise.models import ReleaseInfo, SoftwareQuery
from furl_ai_exercise.service import run_release_graph
from tests.scenario_data import (
    PINNED_WINDOWS10_DOWNLOAD_URL,
    PINNED_WINDOWS10_RELEASE_NOTES_URL,
    PINNED_WINDOWS10_VERSION,
)


def test_firefox_windows10_pinned_release():
    query = SoftwareQuery(
        vendor="Mozilla",
        software="Firefox",
        os_name="Windows",
        os_version="10",
        cpu_arch="x86_64",
        version=PINNED_WINDOWS10_VERSION,
    )
    response = (
        "{\n"
        f"  \"release_notes_url\": \"{PINNED_WINDOWS10_RELEASE_NOTES_URL}\",\n"
        f"  \"download_url\": \"{PINNED_WINDOWS10_DOWNLOAD_URL}\",\n"
        f"  \"version\": \"{PINNED_WINDOWS10_VERSION}\"\n"
        "}"
    )
    llm = RunnableLambda(lambda _prompt: response)

    result = run_release_graph(query, llm)

    assert result == ReleaseInfo(
        release_notes_url=PINNED_WINDOWS10_RELEASE_NOTES_URL,
        download_url=PINNED_WINDOWS10_DOWNLOAD_URL,
        version=PINNED_WINDOWS10_VERSION,
    )
