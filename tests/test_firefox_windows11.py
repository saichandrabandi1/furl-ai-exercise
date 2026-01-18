from langchain_core.runnables import RunnableLambda

from furl_ai_exercise.models import ReleaseInfo, SoftwareQuery
from furl_ai_exercise.service import run_release_graph


def test_firefox_windows11_latest_release():
    query = SoftwareQuery(
        vendor="Mozilla",
        software="Firefox",
        os_name="Windows",
        os_version="11",
        cpu_arch="x86_64",
    )
    response = (
        "{\n"
        "  \"release_notes_url\": \"https://www.mozilla.org/en-US/firefox/notes/latest/\",\n"
        "  \"download_url\": \"https://download.mozilla.org/?product=firefox-latest-ssl&os=win&lang=en-US\",\n"
        "  \"version\": \"latest\"\n"
        "}"
    )
    llm = RunnableLambda(lambda _prompt: response)

    result = run_release_graph(query, llm)

    print(result)
    assert isinstance(result, ReleaseInfo)
    assert result.release_notes_url.startswith("https://www.mozilla.org/")
    assert result.download_url.startswith("https://download.mozilla.org/")
    assert result.version
