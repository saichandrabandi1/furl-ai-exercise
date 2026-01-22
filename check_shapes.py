from furl_ai_exercise.models import SoftwareQuery, ReleaseInfo
from furl_ai_exercise.service import run_release_graph
from langchain_openai import ChatOpenAI

# Create a sample input
query = SoftwareQuery(
    vendor="Mozilla",
    software="Firefox",
    os_name="Windows",
    os_version="11",
    cpu_arch="x86_64"
)

# Initialize model (you can skip this if you just want to test structure)
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Run the function
result = run_release_graph(query, llm)

# Print input and output shapes
print("Input shape:", query.__dict__)
print("\nOutput shape:", result.__dict__)
