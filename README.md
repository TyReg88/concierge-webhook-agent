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

1. **Agent Skills (Tool Use):** The agent is equipped with deterministic Python functions (skills). It autonomously decides when to invoke tools like `get_home_state()` to query the simulated environment before generating a final response.
2. **Context Management & Mapping:** The system effectively maps unstructured natural language inputs (e.g., "turn on the light in the basement") to strict technical system entity IDs (e.g., `base`).
3. **Security Features (Data Minimization & Isolation):** By isolating the agent's logic into a simulated sandbox environment, the architecture demonstrates secure design principles. The agent operates without requiring direct access to a physical core switch or gateway, eliminating the risk of internal network compromise.

## Setup & Testing
*(Hier fügen wir später die konkreten Befehle zum Starten des Python-Skripts und zum Senden eines simulierten cURL-Requests ein.)*