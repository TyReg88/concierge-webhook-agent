# Concierge Webhook Agent

## Overview
This repository contains a Capstone Project for the "5-Day AI Agents: Intensive Vibe Coding Course With Google" hosted on Kaggle. 

It falls under the project category: **Concierge Agents** – *Design safe and useful personal assistants that simplify everyday life, such as planning, organization, or managing personal tasks while keeping user data secure.*

## Real-World Problem & Project Intention
Standard commercial voice assistants often rely on rigid, pre-defined command structures. They lack the contextual awareness to understand natural, conversational requests or complex smart home architectures. This creates a bottleneck where users must memorize exact device names and specific phrases. 

**The Intention:** This project aims to bridge that gap by building an AI-driven intent dispatcher. It acts as an intelligent middleware that parses unstructured human language, understands the implicit context of the request, and maps it to strict, technical system entity IDs (e.g., translating "It's too dark in the living room" to an API call targeting `light.ground_livingroom_sofa`). While this repository uses mocked endpoints for privacy and to facilitate rapid prototyping, the core logic is designed to serve as the foundation for a real-world, privacy-focused voice dispatcher.

## Project Architecture & Workflow
This project acts as an AI interface proxy (Webhook). It is designed to receive JSON payloads representing natural language intents (e.g., voice commands directed at a smart home system), process the context, and autonomously decide which internal tools to call to generate an appropriate response.

**Privacy & Security First:**
To strictly protect private infrastructure data, this repository is completely decoupled from any physical hardware or real L2/L3 network layers. All environmental states, camera detections, and device statuses are simulated using static JSON mock data. No private IP addresses or live camera feeds are exposed or processed in this public repository.

## Development Methodology
The project was entirely conceptualized and implemented using an AI-assisted workflow:
* **Architecture & Strategy:** System design, architectural routing, and general troubleshooting were mapped out via Gemini Chat.
* **Implementation:** The codebase was generated and iterated upon using the **Antigravity IDE**, strictly applying the Vibe Coding principles taught in the course.

## Demonstrated Key Concepts
The agent architecture demonstrates the following key concepts from the course:

1. **Agent Skills (Tool Use):** The agent is equipped with deterministic Python functions (skills). It autonomously decides when to invoke basic tools like `get_home_state()` or custom-coded scenes like `good_morning()` and `good_night()` (which execute underlying modular scripts to manipulate cover states) before generating a final response.
2. **Context Management & Mapping:** The system effectively maps unstructured natural language inputs (e.g., "turn on the light in the basement") to strict technical system entity IDs (e.g., `base`).
3. **Security Features (Data Minimization & Isolation):** By isolating the agent's logic into a simulated sandbox environment, the architecture demonstrates secure design principles. The agent operates without requiring direct access to a physical core switch or gateway, eliminating the risk of internal network compromise.

## Setup & Testing

**Security Notice (Credential Management):**
To fulfill the security requirements of a Concierge Agent, all sensitive credentials (such as the Google Gemini API key) are strictly excluded from version control. The application utilizes `python-dotenv` for local environment variable management.

**1. Environment Setup**
Duplicate the template file to create your local configuration:
`cp .env.example .env`
Open the `.env` file and insert your valid Gemini API key.

**2. Start the Server**
create virtual environment (`python -m venv .venv`),
Ensure all requirements are installed (`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`),
activate virtual environment (`.venv\Scripts\activate`),
then start the FastAPI application via uvicorn (`uvicorn main:app --reload`).


### Troubleshooting

#### PowerShell Script Execution Error (Windows)
If you get a security error when activating the virtual environment in PowerShell (`Activate.ps1 cannot be loaded because running scripts is disabled`), you can allow script execution for your current terminal session by running:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
Then activate the environment:
```powershell
.venv\Scripts\Activate.ps1
```

#### Windows ARM64 / Snapdragon Dependency Issues
If the dependency installation fails on Windows ARM64 (e.g. Snapdragon devices) while building the `cryptography` package from source (due to missing Rust compiler or OpenSSL environment), install a precompiled, compatible wheel first:
```powershell
.\.venv\Scripts\pip.exe install cryptography --only-binary=:all:
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```