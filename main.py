# -----------------------------
# main.py
# Core logic & agents
# -----------------------------

import inspect
import re
from phi.agent import Agent
from phi.model.ollama import Ollama

# Ensure backward compatibility for getargspec
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

# -----------------------------
# Helper Functions
# -----------------------------
def extract_code(text: str) -> str:
    if not text:
        return ""
    python_block = re.search(r"```python\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if python_block:
        return python_block.group(1).strip()
    generic_block = re.search(r"```\s*(.*?)```", text, re.DOTALL)
    if generic_block:
        return generic_block.group(1).strip()
    return text.replace("```", "").strip()

def run_agent(agent: Agent, prompt: str) -> str:
    try:
        response = agent.run(prompt)
        return response.content.strip() if response and response.content else ""
    except Exception as e:
        return f"[ERROR] {agent.name}: {e}"

# -----------------------------
# LLM Model
# -----------------------------
llm = Ollama(
    id="tinyllama",
    temperature=0.3,
    top_p=0.9
)

# -----------------------------
# Agents
# -----------------------------
generator = Agent(
    name="Generator",
    model=llm,
    instructions=[
        "Generate clean and correct Python code based on the prompt.",
        "Return ONLY code.",
        "Wrap code in ```python```."
    ],
    markdown=True
)

qa_agent = Agent(
    name="QA",
    model=llm,
    instructions=[
        "Analyze the generated code for logical errors and edge cases.",
        "Suggest fixes if issues are found.",
        "Return the FULL corrected code in ```python```."
    ],
    markdown=True
)

reviewer = Agent(
    name="Reviewer",
    model=llm,
    instructions=[
        "Review the final code for correctness and completeness.",
        "If everything is correct, reply exactly with: STATUS: APPROVED"
    ],
    markdown=True
)

testcase_gen = Agent(
    name="TestCaseGenerator",
    model=llm,
    instructions=[
        "Generate Python test cases using the unittest framework.",
        "Create a unittest.TestCase class.",
        "Each test case must be a separate test method.",
        "Use assertTrue, assertFalse, or assertEqual.",
        "Assume the main function to test is named main_function.",
        "Wrap the FULL unittest code in ```python```."
    ],
    markdown=True
)

use_case_gen = Agent(
    name="UseCaseGenerator",
    model=llm,
    instructions=[
        "Generate exactly 3 real-world use cases.",
        "Format clearly as: Input → Expected Output"
    ],
    markdown=True
)
