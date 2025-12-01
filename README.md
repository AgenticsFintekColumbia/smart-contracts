# Solidity Smart Contract Generator

## Description

An AI-powered autonomous system for **generating**, **validating**, and **refining** Solidity smart contracts from natural language descriptions. This project combines Agentics (IBM Research), CrewAI, Google Gemini 2.0 Flash, and MCP (Model Context Protocol) to create production-grade Solidity contracts with automatic error detection and correction.

The system features:
- **Multi-step agentic pipeline**: Generation → Validation → Refinement → Re-validation
- **Intelligent error handling**: Automatic compilation and deployment testing with LLM-based fixes
- **Structured outputs**: Pydantic-based SmartContract schema with clauses extraction
- **Flexible model selection**: Google Gemini 2.0 Flash or FSM fine-tuned TinyLlama
- **Interactive UI**: Streamlit chat interface with live logs and contract viewer
- **Sandbox deployment**: Local in-memory Ethereum testing via eth-tester

## Deployment Information

- **Project Slug:** `smart-contracts`
- **Deployment URL:** `https://d28ay7eykuuini.cloudfront.net/smart-contracts`
- **Main File:** `app.py`

## Environment Variables Required

- SELECTED_LLM = "gemini" 
- GEMINI_API_KEY = "api key here"
- GEMINI_MODEL_ID = "gemini/gemini-2.0-flash"

## Local Setup

```bash
# Clone repository
git clone https://github.com/AgenticsFintekColumbia/smart-contracts.git
cd smart-contracts

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
git clone git@github.com:IBM/agentics.git
cd agentics
pip install -e .
cd ..
pip install -e .

# Run the Streamlit app
streamlit run app.py
```

## Architecture

### Core Components

**1. MCP Tools** (`agents/mcp_tools.py`)
- `generate_smart_contract`: LLM-based contract generation using Gemini 2.0 Flash
- `generate_smart_contract_pretrained`: Alternative generation using FSM fine-tuned TinyLlama
- `validate_smart_contract`: Compilation and deployment testing using solcx and eth-tester
- `refine_contract`: Error correction using LLM guidance
- `web_search`: DuckDuckGo search for contextual information

**2. Agentic Pipeline** (`agents/agent.py`)
- **Blockchain Developer Agent**: Multi-step reasoning with 10 reasoning steps
- **Task Pipeline**:
  1. **Generate**: Create initial Solidity contract
  2. **Validate**: Compile and deploy test
  3. **Refine** (conditional): Fix errors if validation fails
  4. **Re-validate** (conditional): Test refined contract
- **Memory Management**: Shared state across tasks via CrewAI memory
- **Tool Routing**: Automatic selection of appropriate MCP tools

**3. Streamlit UI** (`app.py`)
- Chat-based contract description input
- Live log streaming with ANSI cleanup
- Code syntax highlighting for Solidity
- Validation status display (compilable/deployable)
- Clause extraction and visualization
- Example prompts for quick start

## Project Structure

```
smart-contracts/
├── app.py                      # Streamlit UI application
├── agents/
│   ├── agent.py               # Agentic pipeline orchestration
│   └── mcp_tools.py           # MCP tool definitions
├── data/                       # Pretraining checkpoints for FSM
│   └── pretraining_code_checkpoints/
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create manually)
└── README.md                  # Original project documentation
```

## Usage Examples

### Example 1: ERC-20 Token
```
Create a complete ERC-20 token smart contract using Solidity and OpenZeppelin. 
The contract must support minting and burning (restricted to the owner), pausing of transfers, 
and safe initialization of name, symbol, and initial supply.
```

### Example 2: DAO Governance
```
Generate a Solidity-based DAO governance contract that supports proposal creation, 
weighted voting, automatic proposal lifecycle transitions, and execution of approved 
proposals once quorum is met.
```

### Example 3: NFT Marketplace
```
Create a secure Solidity smart contract for an NFT marketplace supporting ERC-721 tokens 
with listings, purchases, cancellation, and royalty support (ERC-2981).
```

## Pipeline Methodology

1. **Generation**: User describes contract → LLM generates full Solidity code + clauses
2. **Validation**: 
   - Compile using solc 0.8.20
   - Deploy to in-memory EthereumTester
   - Capture compiler and deployment errors
3. **Refinement** (if errors):
   - Pass exact error logs to LLM
   - LLM reconstructs corrected version
   - Preserve original functionality
4. **Re-validation**: Test refined contract
5. **Output**: Final deployable contract with full logs

## Features

✅ Generate production-grade Solidity contracts from text  
✅ Automatic compilation and deployment testing  
✅ Intelligent error detection and multi-step correction  
✅ Clause extraction and documentation  
✅ Live log streaming in web UI  
✅ Multiple LLM backends (Gemini, fine-tuned TinyLlama)  
✅ DuckDuckGo search integration  
✅ Structured Pydantic schemas  
✅ Memory-safe task coordination  

## Extending the Project

You can add new MCP tools for:
- Security auditing (e.g., Slither integration)
- Gas optimization analysis
- Static code analysis
- Contract upgrade advisors
- Compliance checkers

Add new tools to `agents/mcp_tools.py` following the FastMCP decorator pattern:
```python
@mcp.tool(name="my_tool_name")
def my_tool(param1: str) -> str:
    """Tool description"""
    return result
```

## Team

**Project Team**
- [Chaitya Shah](https://www.linkedin.com/in/chaityas/) | MS in Data Science, Columbia University
- [Chunghyun Han](https://www.linkedin.com/in/chunghyun-han-355b80244/) | MS in Operations Research, Columbia University
- [Nami Jain](https://www.linkedin.com/in/nami-jain/) | MS in Data Science, Columbia University
- [Yegan Dhaivakumar](https://www.linkedin.com/in/yegan-dhaivakumar) | MS in Data Science, Columbia University

**Faculty Advisors**
- [Alfio Gliozzo](https://www.linkedin.com/in/gliozzo/) | Chief Science Catalyst, IBM Research
- [Agostino Capponi](https://www.linkedin.com/in/agostino-capponi-842b41a5/) | Professor, Columbia University