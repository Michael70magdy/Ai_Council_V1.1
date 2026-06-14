import asyncio
import os
import re
import sys
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Install necessary packages
!pip install litellm nest_asyncio sentence-transformers

import litellm
import nest_asyncio

nest_asyncio.apply()

# =====================================================================
# ƒ– WINDOWS ASYNCIO POLICY PATCH (Configures Selector for Windows)
# =====================================================================
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# =====================================================================

# =====================================================================
# ƒ„ DIRECT API KEY ASSIGNMENT (Bypasses Windows Terminal Environment)
# =====================================================================
os.environ["Gemma_API_KEY"] = "AQ.Ab8RN6J_rjnc7cAe0UbxBu9i6JdJBgL3WJQ3tntZuflJfwTSpQ"
os.environ["GEMINI_API_KEY"] = "AQ.Ab8RN6LhyGu67tqXprY2R_0FuCR03WmXf_TsQvSUHzLbDGHc5Q"
# =================================================0====================

# =====================================================================
# ƒ„ RAG (Retrieval Augmented Generation) Enhancement
# =====================================================================
print("Loading Sentence Transformer model...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("Model loaded.")

# Sample knowledge base for demonstration
knowledge_base = {
    "apple_company": "Apple Inc. is an American multinational technology company headquartered in Cupertino, California. It designs, develops, and sells consumer electronics, computer software, and online services. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the Apple Watch smartwatch, the Apple Vision Pro mixed-reality headset, and the AirPods wireless earbuds. Its services include the App Store, Apple Music, Apple TV+, and iCloud. Founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.",
    "quantum_computing": "Quantum computing is a type of computation that harnesses the phenomena of quantum mechanics, such as superposition and entanglement, to solve complex problems that classical computers cannot. It involves qubits, which can represent 0, 1, or both simultaneously. Major players include IBM, Google, and Microsoft.",
    "software_testing_qa_qc": "In software testing, QA (Quality Assurance) is a proactive process focused on preventing defects throughout the development lifecycle, ensuring quality by establishing processes and standards. QC (Quality Control) is a reactive process focused on identifying defects in the finished product through testing and inspection. QA focuses on 'how to prevent bugs', while QC focuses on 'how to find bugs'.",
    "artificial_intelligence": "Artificial intelligence (AI) is a broad field of computer science that gives computers the ability to perform human-like tasks, such as learning, problem-solving, and decision-making. Machine learning is a subset of AI that uses statistical techniques to enable systems to 'learn' from data without being explicitly programmed.",
    "large_language_models": "Large Language Models (LLMs) are a type of artificial intelligence program that can recognize and generate text, among other tasks. They are trained on vast amounts of text data, allowing them to understand and generate human-like language. Examples include GPT series, LaMDA, and PaLM."
}

# Generate embeddings for the knowledge base documents
print("Generating embeddings for the knowledge base...")
knowledge_base_embeddings = {
    key: embedding_model.encode(value, convert_to_tensor=True)
    for key, value in knowledge_base.items()
}
print("Embeddings generated.")

async def retrieve_context(query: str) -> str:
    """
    Retrieves the most semantically similar context from the knowledge base
    using sentence embeddings and cosine similarity.
    """
    query_embedding = embedding_model.encode(query, convert_to_tensor=True)

    highest_similarity = -1
    best_context_key = None

    for key, doc_embedding in knowledge_base_embeddings.items():
        similarity = cosine_similarity(query_embedding.reshape(1, -1), doc_embedding.reshape(1, -1))[0][0]
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_context_key = key

    # Define a similarity threshold for returning context
    # You might need to tune this threshold based on your dataset
    similarity_threshold = 0.5

    if highest_similarity > similarity_threshold and best_context_key is not None:
        print(f"Retrieved context for query: '{query[:50]}...' with similarity: {highest_similarity:.2f}")
        return knowledge_base[best_context_key]
    else:
        print(f"No relevant context found for query: '{query[:50]}...' (highest similarity: {highest_similarity:.2f})")
        return "No specific external context found for this query."
# =====================================================================

async def get_model_response(model_name: str, prompt: str) -> dict:
    """
    Calls a single LLM asynchronously. Instructs the model to output its response
    and a self-evaluated confidence score inside a clean layout structure.
    """
    # Integrate RAG context into the prompt
    external_context = await retrieve_context(prompt)
    if external_context and external_context != "No specific external context found for this query.":
        context_injection = f"\n\n### EXTERNAL CONTEXT (Provided by RAG System):\n{external_context}\n\n"
    else:
        context_injection = ""

    scoring_system_prompt = f"""
    Before answering:

    * Do not present assumptions as facts.

    * If unsure, say so clearly.

    * If you don't know, say "I don't know."

    * Do not invent facts, statistics, sources, quotes, URLs, or references.

    * Distinguish between facts, assumptions, opinions, and estimates.

    * Ask for clarification if information is missing.

    * Do not fill gaps with guesses.

    * Prioritize accuracy over completeness.

    * If multiple interpretations exist, explain them.

    * At the end, provide:

    * Confidence Level (0-100%)

    * Key Uncertainties (if any)

    You are an advanced AI agent. Answer the user's prompt thoroughly and accurately.
    {context_injection}
    At the absolute end of your response, you must provide your self-evaluated confidence score based on the factual accuracy of your response.

    You MUST format the score exactly like this on its own new line:
    CONFIDENCE_SCORE: [number between 0 and 100]

    USER PROMPT: {prompt}
    """

    messages = [{"role": "user", "content": scoring_system_prompt}]

    try:
        response = await litellm.acompletion(
            model=model_name,
            messages=messages,
            temperature=0.7
        )

        full_content = response.choices[0].message.content

        # Parse the confidence score out of the response text using regex
        confidence_score = 85.0  # Safe default if parsing fails
        cleaned_content = full_content

        match = re.search(r"CONFIDENCE_SCORE:\s*([\d\.]+)", full_content, re.IGNORECASE)
        if match:
            try:
                confidence_score = float(match.group(1))
                # Strip the structural score line out so it doesn't leak into the final text summary
                cleaned_content = re.sub(r"CONFIDENCE_SCORE:\s*[\d\.]+", "", full_content, flags=re.IGNORECASE).strip()
            except ValueError:
                pass

        return {
            "model": model_name,
            "status": "success",
            "content": cleaned_content,
            "score": round(confidence_score, 2)
        }

    except Exception as e:
        return {"model": model_name, "status": "error", "content": str(e), "score": 0.0}

async def run_parallel_generation(prompt: str, models: list) -> list:
    """
    Fires the prompt to all listed models simultaneously.
    """
    print(f"🚩 Broadcasting prompt to {len(models)} models concurrently...")
    tasks = [get_model_response(model, prompt) for model in models]
    results = await asyncio.gather(*tasks)
    return results

async def synthesize_consensus(original_prompt: str, raw_outputs: list, aggregator_model: str) -> str:
    """
    Stage 2: Takes all successful raw outputs accompanied by their individual
    calculated quality scores, and synthesizes them into a master consensus response.
    """
    successful_responses = [out for out in raw_outputs if out["status"] == "success"]

    if not successful_responses:
        return "❌ Stage 2 Failed: All primary models returned an error state."

    print(f"\n™️ Synthesizing consensus using {aggregator_model}...")

    context_blocks = ""
    for out in successful_responses:
        context_blocks += f"### RESPONSE FROM {out['model']} (Confidence Score: {out['score']}%):\n{out['content']}\n\n"

    synthesis_prompt = f"""
    You are an expert meta-analyst and synthesis agent. Your task is to look at multiple draft answers to a user's question, weigh them by their evaluated confidence scores, find the shared truth, and deliver a single definitive response.

    ORIGINAL USER REQUEST:
    \"{original_prompt}\"

    DRAFT RESPONSES FROM PIPELINE AGENTS (WITH CONFIDENCE RATINGS):
    {context_blocks}

    CRITERIA FOR SYNTHESIS:
    1. Cross-examine the facts: **Give significantly heavier mental weight to models showcasing higher confidence scores.** If a model has a much higher confidence score, prioritize its information, especially on factual points. Ignore low-confidence information if contradicted by high-confidence sources.
    2. Eliminate redundancy: Do not repeat points.
    3. Resolve conflicts: If high-confidence responses present conflicting information, try to identify the most plausible truth or state the conflict if unable to resolve definitively.
    4. Structure cleanly: Deliver a single, complete, polished master response using clear markdown layout. Do not write meta-phrases like \"Model A scored 90% and said this.\" Provide only the final unified truth.
    """

    try:
        response = await litellm.acompletion(
            model=aggregator_model,
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Consensus Aggregation Error: {str(e)}"


async def main():
    """
    Unified loop architecture to preserve an active Windows I/O transport pipeline
    throughout all evaluation stages. Runs inside an interactive while loop.
    """
    target_models = [
        "gemini/gemma-4-26b-a4b-it",
        "gemini/gemini-2.5-flash"
    ]

    aggregator_model = "gemini/gemma-4-26b-a4b-it"

    print("==================================================")
    print("🤖 Welcome To Maikool's Ai Council Tool 🤖")
    print("==================================================")

    while True:
        user_prompt = input("""
📌 Enter your question or request (or type 'exit' to quit): """)

        # Check if the user wants to break out of the session
        if user_prompt.strip().lower() in ['exit', 'quit', 'close']:
            print("\n👋 Closing the session. Goodbye! 👋")
            break

        if not user_prompt.strip():
            print("⚠️ You didn't type anything! Please try again. ⚠️")
            continue

        # STAGE 1: Parallel Evaluation with Self-Scoring
        raw_outputs = await run_parallel_generation(user_prompt, target_models)

        # PRINTING SCORES PRIOR TO GETTING FINAL SYNTHESIS ANSWER
        print("\n📊 --- Primary Models Evaluated & Scored ---")
        print("-" * 55)
        for output in raw_outputs:
            if output['status'] == 'success':
                print(f"🤖 Model  : {output['model']}")
                print(f"📈 Score  : {output['score']}% Confidence")
                print(f"🗄 Preview: {output['content'][:90].strip()}...")
            else:
                print(f"❌ Model  : {output['model']} | Status: FAILED")
                print(f"   ⚠️ Error Details: {output['content'][:80]}...")
            print("-" * 55)

        # STAGE 2: Consensus Synthesis
        final_consensus = await synthesize_consensus(user_prompt, raw_outputs, aggregator_model)

        print("\n👑 FINAL AGGREGATED CONSENSUS ANSWER:")
        print("==================================================")
        print(final_consensus)
        print("==================================================")
        print("\n" + "="*50)

    print("\n⏳ Finishing background task operations... ⏳")

    # SILENT ERROR HANDLER: Mutes Windows socket race conditions during loop shutdown
    loop = asyncio.get_running_loop()
    def silent_exception_handler(loop, context):
        # Ignore transport-level errors that fire during garbage collection
        if "exception" in context and isinstance(context["exception"], (OSError, RuntimeError, AttributeError)):
            return
        # Pass meaningful errors along if they occur elsewhere
        loop.default_exception_handler(context)

    loop.set_exception_handler(silent_exception_handler)

    # Give the transport loop a brief window to complete remaining socket actions gracefully
    await asyncio.sleep(0.2)

# =====================================================================
# --- Main Execution Block ---
# The if __name__ == "__main__" block is not needed in Colab after nest_asyncio.apply()
# We can directly run the main coroutine or the test feature.
asyncio.run(main()) # Uncomment to run the interactive loop
