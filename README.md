# 🤖 Maikool's AI Council – Multi-LLM Consensus & RAG System

A powerful AI orchestration system that combines **multiple Large Language Models (LLMs)**, **Retrieval-Augmented Generation (RAG)**, **confidence-based evaluation**, and **consensus synthesis** into a single intelligent pipeline.

Instead of relying on a single AI model, AI Council acts like a panel of AI experts. Multiple models independently analyze the same prompt, evaluate their confidence levels, and collaborate through a final aggregation stage to produce a higher-quality answer.

This project demonstrates concepts from:

- Multi-Agent AI Systems
- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Confidence-Based Reasoning
- Consensus Intelligence
- Async Programming
- AI Orchestration

---

# 📚 Table of Contents

- [Project Overview](#-project-overview)
- [Core Features](#-core-features)
- [Architecture](#-architecture)
- [Workflow](#-workflow)
- [Technologies Used](#-technologies-used)
- [Project Structure](#-project-structure)
- [Code Breakdown](#-code-breakdown)
- [RAG System](#-rag-system)
- [Model Confidence System](#-model-confidence-system)
- [Consensus Aggregation](#-consensus-aggregation)
- [Installation](#-installation)
- [API Configuration](#-api-configuration)
- [Running the Project](#-running-the-project)
- [How It Works](#-how-it-works)
- [Execution Flow](#-execution-flow)
- [Example Output](#-example-output)
- [Error Handling](#-error-handling)
- [Current Knowledge Base](#-current-knowledge-base)
- [Customization](#-customization)
- [Use Cases](#-use-cases)
- [Security Notes](#-security-notes)
- [Future Improvements](#-future-improvements)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

# 🚀 Project Overview

Traditional AI systems usually rely on a single Large Language Model (LLM) to answer questions.

This project introduces a more advanced architecture:

1. Multiple AI models receive the same prompt simultaneously.
2. A RAG system retrieves relevant contextual information.
3. Context is injected into the prompt when applicable.
4. Each model generates an independent answer.
5. Each model evaluates its own confidence level.
6. A consensus model analyzes all responses.
7. The system produces one final synthesized answer.

The result is a more reliable, context-aware, and intelligent AI pipeline.

---

# ✨ Core Features

## ⚡ Parallel AI Inference

Uses Python AsyncIO to execute multiple LLM requests concurrently.

Benefits:

- Reduced latency
- Faster response generation
- Better scalability
- Efficient resource utilization

---

## 🔍 Retrieval-Augmented Generation (RAG)

Includes a lightweight semantic retrieval system powered by:

- Sentence Transformers
- Embedding Generation
- Cosine Similarity Matching

The retrieved context is automatically injected into prompts before being sent to AI models.

---

## 🧠 Semantic Search

The system converts:

- User queries
- Knowledge base documents

into vector embeddings and calculates semantic similarity to retrieve the most relevant information.

---

## 📊 Confidence-Based Evaluation

Every model is instructed to:

- Answer accurately
- Report uncertainty
- Generate a confidence score

Example:

```text
CONFIDENCE_SCORE: 92
```

This score is later used during consensus generation.

---

## 👑 Consensus Synthesis Engine

A dedicated aggregation model:

- Reviews all responses
- Compares confidence scores
- Identifies common truths
- Resolves contradictions
- Produces a single final answer

---

## 🪟 Windows AsyncIO Compatibility

Includes a Windows-specific event loop policy patch to prevent:

- Socket transport issues
- AsyncIO crashes
- Event loop instability

---

## 🔄 Interactive AI Session

Runs continuously until the user exits.

Supports:

- Multiple conversations
- Continuous prompting
- Graceful shutdown handling

---

# 🏗 Architecture

```text
                          User Prompt
                                │
                                ▼
                ┌─────────────────────────────┐
                │    Semantic RAG Retrieval   │
                └──────────────┬──────────────┘
                               │
                               ▼
                    Context Injection Layer
                               │
                               ▼
        ┌────────────────────────────────────────────┐
        │      Parallel Multi-Model Execution        │
        └───────────────┬─────────────────┬──────────┘
                        │                 │
                        ▼                 ▼
              Gemini 2.5 Flash     Gemma 4 26B
                        │                 │
                        ▼                 ▼
                 Confidence Scoring Layer
                                │
                                ▼
                   Consensus Aggregator
                                │
                                ▼
                      Final AI Response
```

---

# 🔄 Workflow

## Stage 1 — User Input

The user enters a prompt:

```text
What is quantum computing?
```

---

## Stage 2 — Context Retrieval

The RAG system searches the knowledge base using semantic similarity.

If relevant information is found, it is attached to the prompt.

---

## Stage 3 — Parallel Model Execution

All configured models receive the enriched prompt simultaneously.

Example:

```python
target_models = [
    "gemini/gemma-4-26b-a4b-it",
    "gemini/gemini-2.5-flash"
]
```

---

## Stage 4 — Confidence Scoring

Each model:

- Generates an answer
- Self-evaluates confidence
- Reports uncertainties

---

## Stage 5 — Consensus Generation

The aggregation model:

- Compares responses
- Prioritizes higher-confidence information
- Removes redundancy
- Resolves conflicts
- Creates the final answer

---

# 🛠 Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Core Programming Language |
| AsyncIO | Concurrent Execution |
| LiteLLM | Unified LLM Interface |
| Sentence Transformers | Semantic Embeddings |
| Scikit-Learn | Cosine Similarity |
| NumPy | Vector Operations |
| Gemini API | Model Provider |
| Regex | Confidence Extraction |
| nest_asyncio | Notebook Compatibility |
| Prompt Engineering | AI Control Logic |

---

# 📂 Project Structure

```text
project/
│
├── AI_Council.py
├── README.md
└── requirements.txt
```

---

# 🧩 Code Breakdown

## 1️⃣ Dependency Installation

```python
!pip install litellm nest_asyncio sentence-transformers
```

Installs:

- LiteLLM
- Sentence Transformers
- AsyncIO Notebook Support

---

## 2️⃣ Windows AsyncIO Patch

```python
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )
```

Prevents Windows transport-level AsyncIO issues.

---

## 3️⃣ API Key Configuration

```python
os.environ["GEMINI_API_KEY"] = "YOUR_API_KEY"
```

Provides authentication for AI models.

---

## 4️⃣ Knowledge Base Embedding Generation

```python
embedding_model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)
```

Creates semantic vector representations for documents.

---

## 5️⃣ Context Retrieval Engine

```python
async def retrieve_context(query):
```

Responsibilities:

- Encode query
- Calculate similarity
- Find best match
- Return relevant context

---

## 6️⃣ Model Response Pipeline

```python
async def get_model_response():
```

Handles:

- Prompt construction
- Context injection
- Model calls
- Confidence extraction
- Error handling

---

## 7️⃣ Parallel Generation Engine

```python
await asyncio.gather(*tasks)
```

Executes all model requests simultaneously.

---

## 8️⃣ Confidence Extraction

Uses regex parsing:

```python
re.search(
    r"CONFIDENCE_SCORE:\s*([\d\.]+)"
)
```

Extracts numerical confidence scores.

---

## 9️⃣ Consensus Aggregation

```python
async def synthesize_consensus()
```

Responsible for:

- Comparing responses
- Weighting confidence scores
- Resolving conflicts
- Producing the final answer

---

## 🔟 Interactive Session Loop

```python
while True:
```

Allows continuous interaction with the AI Council.

---

# 🔍 RAG System

The project implements a lightweight Retrieval-Augmented Generation pipeline.

### Current Flow

1. User submits query
2. Query converted into embedding
3. Similarity calculated against knowledge base
4. Best match selected
5. Context injected into prompt

### Retrieval Method

```python
cosine_similarity()
```

### Embedding Model

```python
all-MiniLM-L6-v2
```

### Future Upgrades

- FAISS
- Pinecone
- ChromaDB
- Weaviate
- LangChain Retrieval

---

# 📈 Model Confidence System

Every AI model is required to provide:

- Confidence Level
- Key Uncertainties

Example:

```text
Confidence Level: 94%

Key Uncertainties:
- Limited recent information
```

Benefits:

- Response ranking
- Reliability estimation
- Better aggregation decisions

---

# 👑 Consensus Aggregation

The aggregator model acts as:

- Reviewer
- Editor
- Meta-Analyst

It examines:

- Shared facts
- Contradictions
- Confidence scores
- Overall quality

Then generates a unified final answer.

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/ai-council.git
cd ai-council
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install litellm
pip install nest_asyncio
pip install sentence-transformers
pip install scikit-learn
pip install numpy
```

---

# 🔑 API Configuration

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key
GEMMA_API_KEY=your_api_key
```

Recommended usage:

```python
from dotenv import load_dotenv
import os

load_dotenv()
```

Never commit API keys to GitHub.

---

# ▶️ Running the Project

```bash
python AI_Council.py
```

---

# 🧠 How It Works

The project simulates collaborative reasoning among AI systems.

Instead of trusting a single model:

- Multiple models contribute answers
- Confidence scores provide weighting
- A meta-model evaluates consensus
- Retrieved knowledge improves grounding

This mimics:

- Expert panels
- Committee reasoning
- Distributed intelligence systems

---

# 🔄 Execution Flow

```text
User Question
      │
      ▼
RAG Retrieval
      │
      ▼
Context Injection
      │
      ▼
Parallel AI Models
      │
      ▼
Confidence Evaluation
      │
      ▼
Consensus Aggregation
      │
      ▼
Final Answer
```

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
Quantum computing is a computational paradigm
that utilizes quantum mechanical principles...
==================================================
```

---

# ⚠️ Error Handling

The project includes:

- Async exception handling
- Model failure isolation
- Confidence fallback mechanisms
- Windows transport error suppression
- Graceful shutdown handling

Even if one model fails, the remaining models continue participating in consensus generation.

---

# 📚 Current Knowledge Base

The demo knowledge base currently includes:

- Apple Inc.
- Quantum Computing
- Software Testing (QA vs QC)
- Artificial Intelligence
- Large Language Models

Additional topics can easily be added:

```python
knowledge_base["new_topic"] = "Topic Content"
```

---

# 🔧 Customization

## Add More Models

```python
target_models = [
    "gemini/gemma-4-26b-a4b-it",
    "gemini/gemini-2.5-flash",
    "openai/gpt-4",
    "anthropic/claude"
]
```

---

## Change Aggregator Model

```python
aggregator_model = "gemini/gemma-4-26b-a4b-it"
```

---

## Extend Knowledge Base

```python
knowledge_base["automation"] = """
Automation testing improves software quality
through automated execution of test cases.
"""
```

---

# 💡 Use Cases

### Software Testing & QA

- Test Strategy
- Test Automation
- API Testing
- QA Best Practices

### Research

- Technical Research
- Knowledge Aggregation
- AI-Assisted Learning

### Education

- Complex Topic Explanations
- Multi-Perspective Analysis

### Enterprise AI

- Internal Knowledge Systems
- Multi-Agent Decision Support

---

# 🔐 Security Notes

⚠️ Never expose API keys publicly.

Recommended:

- Environment Variables
- .env Files
- Secret Managers

Avoid:

```python
os.environ["GEMINI_API_KEY"] = "secret"
```

Use:

```python
os.getenv("GEMINI_API_KEY")
```

---

# 🔮 Future Improvements

## Planned Features

- Vector Database Integration
- FAISS Support
- Pinecone Support
- ChromaDB Integration
- Web Search Integration
- Source Citations
- Streaming Responses
- Multi-Agent Debate Mode
- Agent Memory
- Voice Interface
- REST API
- Docker Deployment
- Web Dashboard
- Local LLM Support

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Add new feature"
```

4. Push changes

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📜 License

MIT License

Free to use, modify, and distribute.

---

# 👨‍💻 Author

## Michael Magdy Fekry (Maikool)

**Software Testing Engineer | QA Automation Engineer | AI Enthusiast**

### Skills

- Manual Testing
- API Testing
- Selenium
- Appium
- Rest Assured
- TestNG
- Java
- Python
- AI Automation
- Multi-Agent Systems
- Retrieval-Augmented Generation (RAG)

---

⭐ If you found this project useful, consider giving it a star on GitHub!
