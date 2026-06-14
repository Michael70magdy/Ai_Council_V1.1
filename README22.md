# 🤖 Maikool's AI Council Tool

A multi-model AI orchestration system that combines parallel LLM execution, confidence-based evaluation, and consensus synthesis into a single intelligent pipeline.

This project demonstrates how multiple AI models can collaborate together like an "AI Council" to generate more reliable, context-aware, and higher-quality answers.

---

# 📚 Table of Contents

- [Project Overview](#-project-overview)
- [Core Features](#-core-features)
- [Architecture](#-architecture)
- [Workflow](#-workflow)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Code Breakdown](#-code-breakdown)
- [Installation](#-installation)
- [How It Works](#-how-it-works)
- [Execution Flow](#-execution-flow)
- [Example Output](#-example-output)
- [Error Handling](#-error-handling)
- [RAG System](#-rag-system)
- [Model Confidence System](#-model-confidence-system)
- [Consensus Aggregation](#-consensus-aggregation)
- [Future Improvements](#-future-improvements)
- [Security Notes](#-security-notes)
- [License](#-license)

---

# 🚀 Project Overview

Traditional AI systems usually rely on a single Large Language Model (LLM) to answer a question.

This project introduces a more advanced architecture:

1. Multiple AI models receive the same prompt simultaneously
2. Each model generates its own answer independently
3. Each model evaluates its own confidence score
4. A final "aggregator AI" reviews all outputs
5. The aggregator synthesizes a final consensus answer

The result is a smarter and more reliable AI pipeline.

---

# ✨ Core Features

## ⚡ Parallel AI Inference

Uses Python `asyncio` to execute multiple LLM requests concurrently for maximum speed and efficiency.

---

## 🧠 Confidence-Based Evaluation

Every model must self-evaluate its response and provide a confidence score from 0–100.

Example:

```text
CONFIDENCE_SCORE: 92
```

---

## 🔍 RAG Context Injection

Includes a lightweight Retrieval-Augmented Generation (RAG) simulation system.

The system injects external context into prompts before sending them to models.

---

## 👑 Consensus Synthesis Engine

A dedicated aggregation model analyzes:
- All responses
- Their confidence scores
- Shared truths
- Contradictions

Then produces a unified final answer.

---

## 🪟 Windows AsyncIO Compatibility

Includes a Windows event loop patch to prevent:
- transport crashes
- socket race conditions
- event loop instability

---

## 🔄 Interactive Chat Session

Runs continuously in terminal mode until the user exits manually.

---

# 🏗 Architecture

```text
                    ┌──────────────────┐
                    │   User Prompt    │
                    └────────┬─────────┘
                             │
                             ▼
              ┌──────────────────────────┐
              │   Context Retrieval      │
              │   (RAG Simulation)       │
              └────────┬─────────────────┘
                       │
                       ▼
         ┌─────────────────────────────────┐
         │ Parallel Multi-Model Execution  │
         └───────┬───────────────┬────────┘
                 │               │
                 ▼               ▼
      Gemini Flash         Gemma 26B
                 │               │
                 ▼               ▼
         Confidence Scoring Engine
                 │
                 ▼
      Consensus Aggregator Model
                 │
                 ▼
        Final Synthesized Answer
```

---

# 🔄 Workflow

## Stage 1 — User Input

The user enters a question inside the terminal.

Example:

```text
What is quantum computing?
```

---

## Stage 2 — Context Retrieval

The system checks whether external contextual knowledge exists for the topic.

If found, it injects additional information into the prompt.

---

## Stage 3 — Parallel Model Execution

All configured models receive the enhanced prompt simultaneously using asynchronous execution.

---

## Stage 4 — Confidence Scoring

Each model:
- answers the question
- evaluates its own response quality
- outputs a confidence score

---

## Stage 5 — Consensus Synthesis

The aggregator model:
- compares all responses
- prioritizes high-confidence information
- removes redundant content
- resolves contradictions
- creates one final polished answer

---

# 🛠 Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| AsyncIO | Concurrent execution |
| LiteLLM | Unified LLM interface |
| Gemini API | AI model provider |
| Regex | Confidence score extraction |
| nest_asyncio | Jupyter/Colab compatibility |
| Prompt Engineering | Structured AI control |
| RAG Concepts | External knowledge injection |

---

# 📂 Project Structure

```text
project/
│
├── main.py
├── README.md
└── requirements.txt
```

---

# 🧩 Code Breakdown

# 1️⃣ Package Installation

```python
!pip install litellm nest_asyncio
```

Installs:
- LiteLLM
- AsyncIO notebook support

---

# 2️⃣ Windows AsyncIO Patch

```python
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
```

Fixes:
- Windows socket transport issues
- event loop crashes

---

# 3️⃣ API Key Configuration

```python
os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
```

Provides authentication for Gemini models.

---

# 4️⃣ RAG Retrieval Function

```python
def retrieve_context(query: str) -> str:
```

Simulates a Retrieval-Augmented Generation system.

Currently:
- keyword-based retrieval
- static knowledge responses

Future upgrades may include:
- vector databases
- embeddings
- semantic search

---

# 5️⃣ Model Response Function

```python
async def get_model_response()
```

Responsible for:
- sending prompts
- injecting context
- collecting responses
- extracting confidence scores
- handling failures

---

# 6️⃣ Parallel Generation Engine

```python
await asyncio.gather(*tasks)
```

Runs all AI models concurrently.

Benefits:
- lower latency
- faster response generation
- scalable architecture

---

# 7️⃣ Confidence Extraction

Uses regex:

```python
re.search(r"CONFIDENCE_SCORE:")
```

Parses structured scores from model outputs.

---

# 8️⃣ Consensus Aggregator

```python
async def synthesize_consensus()
```

The most important stage.

Responsibilities:
- compare outputs
- weight confidence scores
- synthesize final truth
- resolve contradictions

---

# 9️⃣ Interactive Main Loop

```python
while True:
```

Keeps the AI council running continuously.

Supports:
- multiple conversations
- persistent session
- graceful shutdown

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-council-tool.git
```

---

## Install Dependencies

```bash
pip install litellm nest_asyncio
```

---

# ▶️ Run The Project

```bash
python main.py
```

---

# 🧠 How The AI Council Thinks

The project simulates collaborative reasoning between AI systems.

Instead of trusting one model blindly:
- multiple models contribute opinions
- confidence scores provide weighting
- a meta-model evaluates consensus

This mimics:
- committee reasoning
- expert panel discussions
- distributed intelligence systems

---

# 📊 Example Output

```text
🚩 Broadcasting prompt to 2 models concurrently...

📊 --- Primary Models Evaluated & Scored ---

🤖 Model  : gemini/gemma-4-26b-a4b-it
📈 Score  : 94% Confidence

🤖 Model  : gemini/gemini-2.5-flash
📈 Score  : 89% Confidence

👑 FINAL AGGREGATED CONSENSUS ANSWER:
==================================================
Quantum computing is a computational paradigm...
==================================================
```

---

# ⚠️ Error Handling

The project includes:
- async exception protection
- model failure isolation
- silent Windows transport handling
- fallback confidence scoring

Even if one model fails:
- the system continues operating
- remaining models are still synthesized

---

# 🔍 RAG System

Current implementation:
- keyword matching
- static context retrieval

Example topics:
- Apple Inc.
- Quantum Computing

Future implementations:
- Pinecone
- ChromaDB
- FAISS
- LangChain retrieval pipelines

---

# 📈 Model Confidence System

Every model is forced to self-evaluate.

This allows:
- response ranking
- reliability estimation
- confidence-weighted synthesis

---

# 👑 Consensus Aggregation

The aggregator model acts like:
- a reviewer
- editor
- meta-analyst

It examines:
- factual overlap
- contradictions
- quality
- confidence scores

Then generates the final answer.

---

# 🔮 Future Improvements

## Planned Features

- Real vector database support
- Embedding search
- Streaming responses
- Web dashboard
- Agent memory
- Auto model routing
- Local LLM support
- Voice interaction
- Multi-agent debate system
- Autonomous reasoning chains

---

# 🔐 Security Notes

⚠️ Never expose real API keys publicly.

Recommended:
- `.env` files
- secret managers
- environment variables

---

# 📜 License

MIT License

Free to use, modify, and distribute.

---

# 👨‍💻 Author

Developed by **Maikool**

Focused on:
- AI orchestration
- multi-agent systems
- reasoning pipelines
- consensus intelligence
- advanced prompt engineering
