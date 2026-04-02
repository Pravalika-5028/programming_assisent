import inspect
import re
import streamlit as st
from phi.agent import Agent
from phi.model.ollama import Ollama

# Compatibility patch
if not hasattr(inspect, "getargspec"):
    inspect.getargspec = inspect.getfullargspec

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

llm = Ollama(
    id="tinyllama",
    temperature=0.3,
    top_p=0.9
)

generator = Agent(
    name="Generator",
    model=llm,
    instructions=[
        "Generate clean and correct Python code.",
        "Return ONLY code.",
        "Wrap code in ```python```."
    ],
    markdown=True
)

qa_agent = Agent(
    name="QA",
    model=llm,
    instructions=[
        "Check logic and edge cases.",
        "Fix issues if found.",
        "Return FULL corrected code in ```python```."
    ],
    markdown=True
)

reviewer = Agent(
    name="Reviewer",
    model=llm,
    instructions=[
        "Review final code.",
        "If correct, reply exactly: STATUS: APPROVED"
    ],
    markdown=True
)

testcase_gen = Agent(
    name="TestCaseGenerator",
    model=llm,
    instructions=[
        "Generate unittest test cases.",
        "Assume function name is main_function.",
        "Wrap FULL code in ```python```."
    ],
    markdown=True
)

use_case_gen = Agent(
    name="UseCaseGenerator",
    model=llm,
    instructions=[
        "Generate exactly 3 real-world use cases.",
        "Format: Input → Expected Output"
    ],
    markdown=True
)

st.set_page_config(page_title="Multi-Agent Streamlit App", layout="wide")
st.title("Multi-Agent Code Generator")

prompt = st.text_area("Enter requirement", height=180)

if st.button("Run") and prompt.strip():
    gen_out = run_agent(generator, prompt)
    gen_code = extract_code(gen_out)
    st.subheader("Generated Code")
    st.code(gen_code, language="python")

    qa_out = run_agent(qa_agent, gen_code)
    qa_code = extract_code(qa_out)
    st.subheader("QA Code")
    st.code(qa_code, language="python")

    review_out = run_agent(reviewer, qa_code)
    st.subheader("Reviewer Status")
    st.write(review_out)

    tc_out = run_agent(testcase_gen, qa_code)
    tc_code = extract_code(tc_out)
    st.subheader("Test Cases")
    st.code(tc_code, language="python")

    uc_out = run_agent(use_case_gen, prompt)
    st.subheader("Use Cases")
    st.write(uc_out)
