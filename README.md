# General Agent 🕵🏻‍♂️

## Overview
This project provides a fully functioning general-purpose AI agent using the Hugging Face Spaces platform. It offers a Gradio-based web interface for running the agent on a set of benchmark questions, submitting answers, and viewing results. The agent is evaluated with the GAIA benchmark and leverages advanced tools and models (including LangChain, LangGraph, and SmolAgents) to answer questions, process files, and interact with external APIs.

## Features
- **Gradio Web App**: User-friendly interface for running and evaluating the agent.
- **Agent Framework**: Modular agent setup using LangChain, LangGraph, and SmolAgents.
- **Tool Integration**: Includes tools for web search, Wikipedia, Python code execution, file reading, speech-to-text, YouTube transcript extraction, and more.
- **File Handling**: Automatically downloads and manages files required for specific questions.
- **Automated Submission**: Fetches questions, runs the agent, and submits answers to a remote evaluation server.

## Project Structure
```
app.py                  # Main Gradio app and evaluation logic
langgraph_agent.py      # LangGraph-based agent and tool wiring
tools.py                # Custom and third-party tool definitions
requirements.txt        # Python dependencies
.env                    # Environment variables (API keys, etc.)
README.md               # Project documentation (this file)
```

## Setup
1. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
2. **Configure environment**:
   - Copy `.env` and fill in required API keys and endpoints.
3. **Run the app**:
   ```sh
   python app.py
   ```
   - This will launch the Gradio web interface.

## Usage
1. **Login**: Use the Hugging Face login button in the UI.
2. **Run Evaluation**: Click "Run Evaluation & Submit All Answers" to fetch questions, process them with the agent, and submit answers.
3. **View Results**: The app displays your score and a table of questions with submitted answers.

## Customization
- **Agent Logic**: Modify `langgraph_agent.py` to change agent behavior, add/remove tools, or adjust prompts.
- **Tools**: Add new tools in `tools.py` and register them with your agent.

## Requirements
- Python 3.11+
- See `requirements.txt` for all dependencies.

## Notes
- The app is designed for Hugging Face Spaces but can run locally.
- Ensure all API keys and environment variables are set in `.env`.

## License
This project is intended as a template for educational and evaluation purposes.