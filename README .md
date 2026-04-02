# 🤖 Multi-Agent Code Generator

A Streamlit-based application that uses multiple AI agents (powered by [PhiData](https://github.com/phidatahq/phidata) and [Ollama](https://ollama.com/)) to automatically generate, review, test, and document Python code from a plain-text requirement.

---

## 🧠 How It Works

The app chains five specialized agents in sequence:

```
User Prompt
    │
    ▼
[Generator]       → Generates initial Python code
    │
    ▼
[QA Agent]        → Reviews logic, fixes edge cases
    │
    ▼
[Reviewer]        → Approves or flags issues
    │
    ▼
[TestCaseGenerator] → Writes unittest test cases
    │
    ▼
[UseCaseGenerator]  → Produces 3 real-world use cases
```

---

## 📁 Project Structure

```
multi-agent-code-gen/
├── app.py          # Streamlit UI entry point
├── main.py         # Core agent definitions and helpers
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com/) installed and running locally
- `tinyllama` model pulled via Ollama

```bash
ollama pull tinyllama
```

---

## 🚀 Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/multi-agent-code-gen.git
cd multi-agent-code-gen

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install streamlit phidata ollama
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🧩 Agents Overview

| Agent | Role |
|---|---|
| **Generator** | Generates clean Python code from the user prompt |
| **QA Agent** | Analyzes logic and edge cases, returns corrected code |
| **Reviewer** | Validates the final code and returns `STATUS: APPROVED` |
| **TestCaseGenerator** | Generates `unittest` test cases (assumes `main_function`) |
| **UseCaseGenerator** | Produces 3 real-world use cases in `Input → Output` format |

---

## 📸 App Preview

> Enter a requirement like _"Write a function to check if a number is prime"_ and the pipeline runs automatically.

---

## 🔧 Configuration

All agents use the `tinyllama` model via Ollama with these defaults:

```python
llm = Ollama(
    id="tinyllama",
    temperature=0.3,
    top_p=0.9
)
```

To swap the model, update the `id` field in `main.py` with any model you have pulled via Ollama (e.g., `llama3`, `mistral`, `codellama`).

---

## 📝 Notes

- The app patches `inspect.getargspec` for compatibility with newer Python versions.
- Test cases assume the main function is named `main_function`. Rename accordingly after generation.
- Agent responses may vary based on the model used and prompt complexity.

---

## 📄 License

MIT License. Feel free to use, modify, and distribute.

---

## 🙌 Acknowledgements

- [PhiData](https://github.com/phidatahq/phidata) for the agent framework
- [Ollama](https://ollama.com/) for local LLM inference
- [Streamlit](https://streamlit.io/) for the UI
