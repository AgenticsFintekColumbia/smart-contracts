import re
import streamlit as st
import streamlit.components.v1 as components
import html as _html

# ---------------------------
# Configuration
# ---------------------------
LOG_HEIGHT_PX = 300  # adjust log box height here

# ---------------------------
# 1. LOAD PIPELINE (cached)
# ---------------------------
@st.cache_resource
def get_pipeline():
    from agent import run_contract_pipeline
    return run_contract_pipeline

_ansi_escape = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def clean_ansi(text: str):
    return _ansi_escape.sub("", text or "")


def render_logs_in_placeholder(placeholder, log_text: str, height_px: int = LOG_HEIGHT_PX):
    """Render logs inside a single placeholder using components.html(), autoscrolls to bottom."""
    safe_text = _html.escape(log_text).replace("\n", "<br/>")
    html = f"""
    <div id="log-box" style="
        background-color: #1a1d23;
        color: #fafafa;
        padding: 12px;
        border-radius: 6px;
        height: {height_px}px;
        overflow-y: auto;
        font-family: monospace;
        border: 1px solid #333;
        white-space: pre-wrap;
        overflow-anchor: none;
    ">{safe_text}</div>

    <script>
    setTimeout(function() {{
        var box = document.getElementById("log-box");
        if (box) {{
            box.scrollTop = box.scrollHeight;
        }}
    }}, 20);
    </script>
    """
    placeholder.empty()
    with placeholder:
        components.html(html, height=height_px + 30, scrolling=False)


def render_app():
    # ---------------------------
    # 2. PAGE CONFIG + CSS
    # ---------------------------
    st.set_page_config(
        page_title="Solidity Smart Contract Generator",
        page_icon="🧠",
        layout="wide"
    )

    st.markdown("""
    <style>
    body {
        background-color: #0e1117;
        color: #fafafa;
    }
    .sidebar .sidebar-content {
        background-color: #1a1d23;
    }
    button[kind="primary"] {
        background-color: #4b8bf4 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    .stTextInput > div > div > input {
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------------
    # 3. INTRO SCREEN
    # ---------------------------
    if "show_instructions" not in st.session_state:
        st.session_state.show_instructions = True

    if st.session_state.show_instructions:
        st.title("🧠 Smart Contract Generator")

        st.markdown("""
        ---

        ## 📘 Project Overview
        Smart contract development is complex, error prone, and requires deep knowledge of Solidity, security patterns, compiler behavior, and deployment pipelines. Even minor issues like incorrect modifiers, missing initializations, unsafe state updates can break a contract or introduce vulnerabilities. This application solves that by providing an **AI powered autonomous pipeline** that takes a natural language idea, generates a Solidity contract, validates it through compilation/deployment, fixes errors automatically, and returns a ready to deploy final version.

        ---
                        
        ## 🤖 Why Agentics?
        Traditional prompting cannot reliably produce error free contracts. **Agentics** lets us structure the entire process into deterministic reasoning steps:
        - Dedicated tasks for generation, validation, and refinement  
        - Shared memory so each step has context  
        - Automatic triggering of refinement only when errors exist  
        - Pydantic schemas ensuring structured SmartContract objects  
        - MCP tool calling for accurate compilation, deployment, and LLM based fixes  

        This transforms the LLM into a controlled, verifiable system rather than free form text generation.

        ---
                        
        ## 🛠️ Tech Stack 
        **Backend & Agentic System:**
        - <a href="https://github.com/IBM/Agentics" target="_blank">Agentics (IBM Research Repository)</a> — core autonomous agent framework enabling task coordination, memory management, and structured multi-step execution 
        - CrewAI — task execution, memory state, tool routing  
        - Pydantic — structured SmartContract schema  
        - MCP (Model Context Protocol) — connects tools over stdio  
        - Google Gemini 2.0 Flash — main LLM for generation & refinement  
        - FSM Fine-Tuned TinyLlama — alternative lightweight model option 
                        
        **Tools:**  
        - `generate_smart_contract` – initial creation  
        - `validate_smart_contract` – compile + deploy checks  
        - `refine_contract` – automated correction using LLM  
        - DDG search tool for contextual info  
                        
        **Frontend:**  
        - Streamlit UI with dynamic HTML log rendering and custom contract viewer  

        **Environment:**  
        - Python 3.12  
        - uvx runtime  
        - `.env` configuration loader  

        ---

        ## ⚙️ Methodology
        The contract pipeline follows a strict three-stage autonomous loop:

        **1) Generation** – The LLM converts your description into a full Solidity contract (with events, modifiers, comments, and clauses).  
        **2) Validation** – The contract is compiled and deployed in a sandbox, producing structured results (`is_compilable`, `is_deployable`, `compiler_errors`, `deploy_errors`).  
        **3) Refinement** – If *any* error exists, the LLM receives the exact error logs and reconstructs a corrected version while preserving the original functionality.

        This continues until a deployable contract is produced or the pipeline completes with the final best version.

        ---

        ## 🚀 How to Use This App
        **1. Describe the contract idea** — the more detail you add, the better the final code.  
        **2. Click "Generate Contract"** — the system begins the multi-step pipeline.  
        **3. Watch the live logs** — generation, compilation, deployment, error messages, refinements.  
        **4. Review results** — final Solidity code, clauses, validation status, and all logs.

        The tool is ideal for learning, prototyping, auditing, and rapid contract development.

        ---

        ## 👥 Collaborators
        <div style="font-size: 0.9rem; color: #cccccc;">
        <strong>Project Team</strong><br/>
        <a href="https://www.linkedin.com/in/chaityas/" target="_blank">Chaitya Shah</a> | MS in Data Science, Columbia University<br/>
        <a href="https://www.linkedin.com/in/chunghyun-han-355b80244/" target="_blank">Chunghyun Han</a> | MS in Operations Research, Columbia University<br/>
        <a href="https://www.linkedin.com/in/nami-jain/" target="_blank">Nami Jain</a> | MS in Data Science, Columbia University<br/>
        <a href="https://www.linkedin.com/in/yegan-dhaivakumar" target="_blank">Yegan Dhaivakumar</a> | MS in Data Science, Columbia University<br/><br/>

        <strong>Faculty Advisors</strong><br/>
        <a href="https://www.linkedin.com/in/gliozzo/" target="_blank">Alfio Gliozzo</a> | Chief Science Catalyst, IBM Research<br/>
        <a href="https://www.linkedin.com/in/agostino-capponi-842b41a5/" target="_blank">Agostino Capponi</a> | Professor, Columbia University<br/>
        </div>

        [![GitHub Repo](https://img.shields.io/badge/GitHub-Repository-blue?logo=github)](https://github.com/AgenticsFintekColumbia/smart-contracts/)
               
        ---

            
        """, unsafe_allow_html=True)
        

        col1, col2, col3 = st.columns([5, 2, 5])

        with col2:
            if st.button("Got it!", use_container_width=True):
                st.session_state.show_instructions = False


        st.stop()

    # ---------------------------
    # 4. SESSION STATE
    # ---------------------------
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "crew_log" not in st.session_state:
        st.session_state.crew_log = ""

    # ---------------------------
    # 6. SIDEBAR
    # ---------------------------
    with st.sidebar:
        st.header("💬 Chat Assistant / Model")

        EXAMPLE_PROMPTS = {
            "Create a Full ERC-20 Token (Mint/Burn/Pause)": "Create a complete ERC-20 token smart contract using Solidity and OpenZeppelin. The contract must support minting and burning (restricted to the owner), pausing of transfers, and safe initialization of name, symbol, and initial supply. Include clear comments, NatSpec documentation, and ensure the contract follows security best practices and gas-efficient design patterns.",

            "Build a DAO with Voting + Proposal Execution": "Generate a Solidity-based DAO governance contract that supports proposal creation, weighted voting, automatic proposal lifecycle transitions, and execution of approved proposals once quorum is met. The contract should include events, role restrictions, protections against re-entrancy, and clear architectural comments and NatSpec to make it upgrade-friendly and secure.",

            "NFT Marketplace with Listings + Sales + Royalties": "Create a secure Solidity smart contract for an NFT marketplace supporting ERC-721 tokens. It must enable NFT listings, purchases, cancellation of listings, and royalty support (ERC-2981 if available). Use safe payment patterns, prevent re-entrancy, track listings efficiently, emit all necessary events, and include high-quality comments and NatSpec documentation throughout the contract."
        }

        st.write("### Example Prompts")

        for label, long_prompt in EXAMPLE_PROMPTS.items():
            if st.button(label):
                st.session_state["chat_input"] = long_prompt

        MODEL_OPTIONS = {
            "Gemini 2.0 Flash": "gemini",
            "FSM Fine-Tuned TinyLlama": "fsm_pretrained",
            # "GPT-4": "gpt4",
            # "Claude 3.5": "claude_3_5",
        }

        model_label = st.selectbox("Choose generation model", list(MODEL_OPTIONS.keys()))
        selected_model = MODEL_OPTIONS[model_label]

        user_input = st.text_area("Ask or refine your contract...", key="chat_input", height=200)

    # ---------------------------
    # 7. MAIN APP
    # ---------------------------
    st.title("🧠 Solidity Contract Generator")

    if st.button("Generate Contract", key="generate_contract"):
        if not user_input.strip():
            st.warning("Please enter a contract description.")
            st.stop()

        st.chat_message("user").write(user_input)

        with st.chat_message("assistant"):
            st.write("Running Agent...")

            log_placeholder = st.empty()
            st.session_state.crew_log = ""
            render_logs_in_placeholder(log_placeholder, "Waiting for logs...", LOG_HEIGHT_PX)

            pipeline = get_pipeline()

            def _handle_log_stream(log_text: str):
                st.session_state.crew_log = clean_ansi(log_text)
                render_logs_in_placeholder(
                    log_placeholder, st.session_state.crew_log, LOG_HEIGHT_PX
                )

            with st.spinner("Generating contract..."):
                result, final_log = pipeline(
                    user_input,
                    model_choice=selected_model,
                    on_log=_handle_log_stream,
                )

            st.session_state.crew_log = clean_ansi(final_log or st.session_state.crew_log)
            render_logs_in_placeholder(log_placeholder, st.session_state.crew_log, LOG_HEIGHT_PX)

            # ---------------------------
            # Result is already extracted from agent.py
            # ---------------------------
            final_contract = result
            
            # Handle unexpected result types
            if not hasattr(final_contract, "contract_code"):
                st.error(f"❌ No valid contract returned. Result type: {type(final_contract).__name__}")
                if isinstance(final_contract, dict):
                    st.error(f"Available keys: {list(final_contract.keys())}")
                st.stop()

            # Save to chat history
            st.session_state.chat_history.append(
                {"user": user_input, "contract": final_contract}
            )

            # ---------------------------
            # FINAL OUTPUT
            # ---------------------------
            st.success("Generated Contract")

            st.subheader("📖 Clauses")
            clauses = getattr(final_contract, "clauses", [])
            if clauses:
                for clause in clauses:
                    title = getattr(
                        clause,
                        "title",
                        clause.get("title") if isinstance(clause, dict) else None,
                    )
                    desc = getattr(
                        clause,
                        "description",
                        clause.get("description") if isinstance(clause, dict) else None,
                    )
                    st.write(f"• **{title}** — {desc}")
            else:
                st.write("No clauses found.")

            if final_contract and hasattr(final_contract, "contract_code"):
                st.code(final_contract.contract_code, language="solidity")
            else:
                st.write("⚠️ No contract code returned.")

            st.subheader("🧪 Validation Results")
            is_compilable = getattr(final_contract, "is_compilable", None)
            is_deployable = getattr(final_contract, "is_deployable", None)
            compiler_errors = getattr(final_contract, "compiler_errors", "")
            deploy_errors = getattr(final_contract, "deploy_errors", "")

            if is_compilable:
                st.success("Contract is compilable")
            else:
                st.error(f"Contract failed compilation: \n{compiler_errors}")

            if is_deployable:
                st.success("Contract is deployable")
            else:
                st.error(f"Contract failed deployment: \n{deploy_errors}")

if __name__ == "__main__":
    render_app()