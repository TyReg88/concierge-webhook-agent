### Core Architecture Overview

1. **Simulated Home State ([mock_state.json]):**
   * Acts as the single source of truth for the simulated Home Assistant environment. 
   * It maps physical devices (lights, window covers, cameras) to Home Assistant structures like `entity_id` (e.g., `light.ground_livingroom_sofa`), `friendly_name`, `domain`, `floor`, and `state`.

2. **FastAPI Server Control Endpoints ([main.py]):**
   * **`GET /state`**: Reads and returns the contents of [mock_state.json]
   * **`POST /webhook`**: Receives natural language voice or text commands via a JSON payload: `{"query": "Es ist zu dunkel im Wohnzimmer beim Sofa, mach bitte das Licht an."}`.

3. **Intelligent Processing Loop (Dual-Path Execution):**
   When a request hits the webhook, the server processes it in one of two ways:
   * **Primary Path (Gemini Agent):** 
     * Uses `gemini-3.1-flash-lite` with **Automatic Function Calling (AFC)**.
     * The model is provided with two Python functions as tools: `get_home_state` and `set_device_state`.
     * The model dynamically decides to run `get_home_state` to inspect the rooms, matches the fuzzy natural language (e.g., "Sofa") to the precise entity ID (`light.ground_livingroom_sofa`), triggers `set_device_state`, and generates a natural response.
   * **Fallback Path (Local Dispatcher):**
     * If the Gemini API key is missing or the API returns an error (such as rate limits or network issues), the app gracefully redirects the query to `fallback_dispatcher`.
     * This uses local regex/keyword matching to perform the state changes offline, ensuring the application never crashes and remains responsive.