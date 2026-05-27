import asyncio
import os
import re
import sys

# Install necessary packages
!pip install litellm nest_asyncio

import litellm
import nest_asyncio

nest_asyncio.apply()

# =====================================================================
# ƒ WINDOWS ASYNCIO POLICY PATCH (Configures Selector for Windows)
# =====================================================================
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
# =====================================================================

# =====================================================================
# ƒ DIRECT API KEY ASSIGNMENT (Bypasses Windows Terminal Environment)
# =====================================================================
os.environ["Gemma_API_KEY"] = "##"
os.environ["GEMINI_API_KEY"] = "##"
# =====================================================================

# =====================================================================
# ƒ RAG (Retrieval Augmented Generation) Placeholder
# =====================================================================
def retrieve_context(query: str) -> str:
    """
    Simulates a RAG system by returning a relevant context based on the query.
    In a real application, this would query a knowledge base or search engine.
    """
    if "apple company" in query.lower() or "apple inc" in query.lower():
        return """Apple Inc. is an American multinational technology company headquartered in Cupertino, California. It designs, develops, and sells consumer electronics, computer software, and online services. Its hardware products include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the Apple Watch smartwatch, the Apple Vision Pro mixed-reality headset, and the AirPods wireless earbuds. Its services include the App Store, Apple Music, Apple TV+, and iCloud.
        Founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976.
        """
    elif "quantum computing" in query.lower():
        return """Quantum computing is a type of computation that harnesses the phenomena of quantum mechanics, such as superposition and entanglement, to solve complex problems that classical computers cannot. It involves qubits, which can represent 0, 1, or both simultaneously.
        Major players include IBM, Google, and Microsoft.
        """
    else:
        return "No specific external context found for this query."
# =====================================================================

async def get_model_response(model_name: str, prompt: str) -> dict:
    """
    Calls a single LLM asynchronously. Instructs the model to output its response
    and a self-evaluated confidence score inside a clean layout structure.
    """
    # Integrate RAG context into the prompt
    external_context = retrieve_context(prompt)
    if external_context and external_context != "No specific external context found for this query.":
        context_injection = f"\n\n### EXTERNAL CONTEXT (Provided by RAG System):\n{external_context}\n\n"
    else:
        context_injection = ""

    scoring_system_prompt = f"""
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
        print("\n📊 --- Primary Models Evaluated & Scored --- 📊")
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
