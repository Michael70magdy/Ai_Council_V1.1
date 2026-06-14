# 🤖 AI Council – Multi-LLM Consensus & RAG System

AI Council is an advanced AI orchestration system that combines multiple Large Language Models (LLMs), Retrieval-Augmented Generation (RAG), confidence scoring, and consensus synthesis to produce more reliable and accurate answers.

Instead of relying on a single AI model, AI Council consults multiple models simultaneously, evaluates their confidence levels, enriches responses with retrieved knowledge, and generates a final consensus answer.

---

## 🚀 Features

### 🧠 Multi-Model AI Council
- Sends prompts to multiple AI models in parallel.
- Collects independent responses from each model.
- Supports easy integration of additional LLM providers.

### 🔍 Retrieval-Augmented Generation (RAG)
- Uses Sentence Transformers for semantic search.
- Retrieves relevant context from a knowledge base before querying models.
- Enhances factual accuracy and reduces hallucinations.

### 📊 Confidence-Based Evaluation
- Each model self-evaluates its response.
- Extracts confidence scores automatically.
- Displays confidence levels for comparison.

### 👑 Consensus Synthesis Engine
- Analyzes all model responses.
- Gives greater weight to higher-confidence outputs.
- Resolves conflicts and removes redundancy.
- Produces a single polished answer.

### ⚡ Fully Asynchronous Processing
- Executes multiple model calls concurrently using AsyncIO.
- Faster than sequential model execution.
- Scalable architecture for larger AI councils.

---

## 🏗️ System Architecture

```text
                     User Prompt
                           │
                           ▼
             ┌────────────────────────┐
             │    RAG Retrieval       │
             └────────────────────────┘
                           │
                           ▼
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
     Model A            Model B            Model N
    (Gemma)            (Gemini)          (Future)
        │                  │                  │
        └──────────┬───────┴───────┬──────────┘
                   ▼               ▼
          Confidence Scoring Layer
                           │
                           ▼
             Consensus Aggregation
                           │
                           ▼
                Final AI Response
```

---

## 🛠️ Technologies Used

- Python
- AsyncIO
- LiteLLM
- Sentence Transformers
- Scikit-Learn
- NumPy
- Gemini API
- Gemma Models
- Nest AsyncIO

---

## 📦 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ai-council.git
cd ai-council
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install litellm
pip install nest_asyncio
pip install sentence-transformers
pip install scikit-learn
pip install numpy
```

Or create a requirements file and run:

```bash
pip install -r requirements.txt
```

---

## 🔑 API Configuration

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key
GEMMA_API_KEY=your_api_key
```

Load them securely:

```python
from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMMA_API_KEY = os.getenv("GEMMA_API_KEY")
```

> **Important:** Never commit API keys to GitHub.

---

## ▶️ Running the Application

```bash
python AI_Council.py
```

Example:

```text
==================================================
🤖 Welcome To Maikool's AI Council Tool 🤖
==================================================

📌 Enter your question:

What is quantum computing?
```

---

## 🔍 Example Workflow

### User Query

```text
What is the difference between QA and QC?
```

### RAG Retrieval

The system searches the knowledge base and retrieves the most relevant context.

### Model Responses

```text
Gemma:
Confidence Score: 91%

Gemini:
Confidence Score: 88%
```

### Consensus Generation

The aggregation model synthesizes all responses into a single final answer.

```text
QA focuses on preventing defects through processes and standards,
while QC focuses on identifying defects through testing and inspection.
```

---

## 📚 Current Knowledge Base

The demo knowledge base includes:

- Apple Inc.
- Quantum Computing
- Software Testing (QA vs QC)
- Artificial Intelligence
- Large Language Models (LLMs)

Additional entries can be added easily:

```python
knowledge_base = {
    "topic_name": "knowledge content"
}
```

---

## 🔧 Customization

### Add More Models

```python
target_models = [
    "gemini/gemma-4-26b-a4b-it",
    "gemini/gemini-2.5-flash",
    "openai/gpt-4",
    "anthropic/claude"
]
```

### Change Aggregator Model

```python
aggregator_model = "gemini/gemma-4-26b-a4b-it"
```

### Extend Knowledge Base

```python
knowledge_base["software_automation"] = """
Automation testing improves software quality by
executing tests automatically using tools and frameworks.
"""
```

---

## 🔒 Security Best Practices

### ❌ Avoid

```python
os.environ["GEMINI_API_KEY"] = "your-secret-key"
```

### ✅ Recommended

```python
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

---

## ⚠️ Limitations

- Confidence scores are self-reported by models.
- Knowledge base is currently local and static.
- No vector database integration.
- Consensus quality depends on model outputs.
- Requires valid API credentials.

---

## 🎯 Future Enhancements

- FAISS Integration
- Pinecone Support
- ChromaDB Integration
- Web Search Capability
- Citation Generation
- Multi-Agent Debate System
- Response Streaming
- REST API
- Docker Deployment
- Web-Based UI Dashboard

---

## 💡 Use Cases

### Software Testing & QA

- Test Case Generation
- API Testing Guidance
- Automation Framework Advice
- QA Best Practices

### Research & Learning

- AI Concepts
- Technical Topics
- Knowledge Aggregation

### Decision Support

- Technology Comparison
- Solution Evaluation
- Risk Assessment

### Enterprise AI

- Internal Knowledge Retrieval
- Multi-Agent Systems
- AI-Assisted Analysis

---

## 🤝 Contributing

Contributions are welcome!

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

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

### Michael Magdy Fekry

**Software Testing Engineer | QA Automation Engineer | AI Enthusiast**

#### Skills
- Manual Testing
- API Testing
- Selenium
- Appium
- Rest Assured
- TestNG
- Java
- Python
- AI Automation
- Retrieval-Augmented Generation (RAG)

---

⭐ If you found this project useful, please consider giving it a star on GitHub!
