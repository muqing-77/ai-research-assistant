# AI Research Assistant

A multi-round AI research assistant built with Python, Streamlit, OpenAI, and Tavily Search.

This project demonstrates how to build an agent-style LLM system that can:
- generate a research plan
- iteratively search for external evidence
- decide whether the current evidence is sufficient
- produce a structured final summary grounded in retrieved information

---

## Overview

Unlike a standard chatbot that answers directly from model knowledge, this system follows a multi-step research workflow:

1. Generate a concise research plan
2. Rewrite the user question into search-friendly queries
3. Perform iterative web search
4. Collect evidence across multiple rounds
5. Check whether the evidence is sufficient
6. Generate a structured final answer

This makes the system more grounded, interpretable, and suitable for research-style question answering.

---

## Features

- Multi-round agent workflow
- Query rewriting for better search quality
- Real-time web search with Tavily
- Evidence aggregation across search rounds
- Structured final summary
- Streamlit web interface
- Search rounds and sources visualization

---

## Project Structure

ai-research-assistant/

├── app.py

├── agent.py

├── tools.py

├── prompts.py

├── requirements.txt

├── README.md

├── .gitignore

├── .env.example

└── assets/
    └── screenshot.png

---

## Tech Stack

- Python
- Streamlit
- OpenAI API
- Tavily Search API
- LangChain
- python-dotenv

---

## How It Works

### 1. Research Planning
The system first generates a short research plan to clarify what should be investigated.

### 2. Iterative Search
Instead of searching only once, the agent can perform multiple search rounds.  
At each round, it generates a new search query based on the original question and previously collected evidence.

### 3. Evidence Sufficiency Check
After each round, the system evaluates whether the current evidence is sufficient to answer the question.

### 4. Final Structured Summary
Once enough evidence has been gathered (or the maximum number of rounds is reached), the system produces a structured final response with the following sections:

- Topic Overview
- Key Findings
- Important Takeaways
- Limitations / Uncertainty

---

## Installation

### Clone the repository:


git clone https://github.com/YOUR_USERNAME/ai-research-assistant.git
cd ai-research-assistant

### Creat and acitvate environment:
conda create -n ai-agent python=3.10 -y
conda activate ai-agent

### Install dependencies:
pip install -r requirements.txt

### Creat a .env file in the project root:
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here

## Run the App


python -m streamlit run app.py
then open:
http://localhost:8501
### Example Questions
What is retrieval-augmented generation and how is it different from fine-tuning?
What is the difference between machine learning and deep learning?
Compare transformers, RNNs, and CNNs for sequence modeling.

## Why This Project Matter
This project goes beyond a simple chatbot by demonstrating:

tool-augmented LLM workflows
iterative retrieval
planning and evidence-based summarization
early-stage agent design

It reflects key ideas used in modern AI assistants and research agents.

## What I learned
Through this project, I learned how to:

design multi-step LLM workflows
integrate external tools into AI systems
improve answer grounding through iterative retrieval
balance model reasoning with tool reliability
build a lightweight AI product interface with Streamlit

## Future Improvements
Add memory for multi-turn conversations
Add support for PDF / document upload
Add richer source ranking and citation formatting
Add multiple tool types beyond web search
Add exportable research reports

## Notes
.env is excluded from version control
API keys should never be committed
search quality depends on the reliability of external search tools
