import os
import json
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from google.genai.errors import APIError
from dotenv import load_dotenv

# Load environment variables from a .env file (override=True ensures .env values take precedence)
load_dotenv(override=True)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("concierge-webhook")


app = FastAPI(
    title="Concierge Webhook Agent",
    description="Intelligent middleware mapping natural language intents to mock system entity IDs.",
    version="1.0.0"
)

MOCK_STATE_PATH = os.path.join(os.path.dirname(__file__), "mock_state.json")

# Pydantic models for API validation
class WebhookRequest(BaseModel):
    query: str

class DeviceStateResponse(BaseModel):
    devices: list

# Tool definitions for Gemini
def get_home_state() -> Dict[str, Any]:
    """
    Returns the current state of all home automation devices in the house.
    This includes device entity_id, friendly_name, state (on/off/open/closed/recording/etc.),
    domain (light/cover/camera/etc.), floor (ground/ext/etc.), and any latest events.
    Always use this tool to inspect the current state of the home before performing actions
    or answering questions about devices.
    """
    try:
        with open(MOCK_STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"devices": []}
    except json.JSONDecodeError:
        return {"error": "Failed to decode mock state file"}

def set_device_state(entity_id: str, state: str) -> Dict[str, Any]:
    """
    Sets the state of a specific device in the home.
    
    Args:
        entity_id: The exact entity_id of the device (e.g. 'light.ground_livingroom_sofa').
        state: The new target state (e.g. 'on', 'off', 'open', 'closed').
        
    Returns:
        A status dictionary indicating success or failure.
    """
    try:
        with open(MOCK_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": "Could not read mock state file"}

    # Find and update the device state
    device_found = False
    for device in data.get("devices", []):
        if device.get("entity_id") == entity_id:
            device["state"] = state
            device_found = True
            break

    if not device_found:
        return {"error": f"Device with entity_id '{entity_id}' not found"}

    try:
        with open(MOCK_STATE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return {"status": "success", "entity_id": entity_id, "state": state}
    except Exception as e:
        return {"error": f"Failed to save updated state: {str(e)}"}


def fallback_dispatcher(query: str) -> Dict[str, Any]:
    """
    Fallback deterministic dispatcher that runs when the Gemini API is unavailable or has billing issues.
    It matches simple keywords to simulate tool calls.
    """
    query_lower = query.lower()
    response_msg = "Ich konnte die Anfrage leider nicht verstehen."
    actions_taken = []
    
    # Check for Sofa Licht
    if "sofa" in query_lower:
        if any(w in query_lower for w in ["an", "on", "dunkel", "dark", "heller"]):
            res = set_device_state("light.ground_livingroom_sofa", "on")
            actions_taken.append(res)
            response_msg = "Ich habe das Sofa Licht eingeschaltet."
        elif any(w in query_lower for w in ["aus", "off", "hell", "light"]):
            res = set_device_state("light.ground_livingroom_sofa", "off")
            actions_taken.append(res)
            response_msg = "Ich habe das Sofa Licht ausgeschaltet."
            
    # Check for Terrassenbeleuchtung
    elif any(w in query_lower for w in ["terrasse", "garden", "terrac", "garten"]):
        if any(w in query_lower for w in ["an", "on"]):
            res = set_device_state("light.ext_garden_terrace", "on")
            actions_taken.append(res)
            response_msg = "Ich habe die Terrassenbeleuchtung eingeschaltet."
        elif any(w in query_lower for w in ["aus", "off"]):
            res = set_device_state("light.ext_garden_terrace", "off")
            actions_taken.append(res)
            response_msg = "Ich habe die Terrassenbeleuchtung ausgeschaltet."
            
    # Check for Küchenfenster Rollladen
    elif any(w in query_lower for w in ["küche", "kitchen", "rollladen", "fenster", "window"]):
        if any(w in query_lower for w in ["auf", "open", "öffn"]):
            res = set_device_state("cover.ground_kitchen_window", "open")
            actions_taken.append(res)
            response_msg = "Ich habe den Rollladen am Küchenfenster geöffnet."
        elif any(w in query_lower for w in ["zu", "close", "schließ"]):
            res = set_device_state("cover.ground_kitchen_window", "closed")
            actions_taken.append(res)
            response_msg = "Ich habe den Rollladen am Küchenfenster geschlossen."
            
    return {
        "status": "success",
        "dispatcher": "rule_based_fallback",
        "query": query,
        "actions": actions_taken,
        "response": response_msg
    }


SYSTEM_INSTRUCTION = (
    "You are a helpful and secure Home Assistant Concierge Agent. "
    "Your job is to translate unstructured natural language commands into home control actions. "
    "Always start by using the get_home_state tool to retrieve the current state of devices. "
    "If the user wants to change a device state, identify the target device entity_id from the state, "
    "then use the set_device_state tool to modify the state of that device. "
    "Always resolve fuzzy requests (like 'Turn off the couch light' or 'It is too dark in the living room') "
    "to the correct specific entity IDs by inspecting the home state first. "
    "Answer politely in the same language the user used (usually German or English)."
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "Concierge Webhook Agent"}

@app.get("/state", response_model=DeviceStateResponse)
async def get_state():
    """Returns the current simulated environment state."""
    return get_home_state()

@app.post("/webhook")
async def process_intent(payload: WebhookRequest):
    """
    Receives a natural language query, processes it with Gemini, 
    and returns the agent's natural response.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY environment variable not set. Falling back to local dispatcher.")
        return fallback_dispatcher(payload.query)
    
    try:
        # Initialize client with the API key from environment
        client = genai.Client(api_key=api_key)
        
        # Call Gemini using automatic function calling
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=payload.query,
            config=types.GenerateContentConfig(
                tools=[get_home_state, set_device_state],
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        
        return {
            "status": "success",
            "dispatcher": "gemini_agent",
            "query": payload.query,
            "response": response.text
        }
        
    except APIError as e:
        logger.error(f"Gemini API Error: {str(e)}. Falling back to local dispatcher.")
        # Attempt fallback instead of crashing
        return fallback_dispatcher(payload.query)
    except Exception as e:
        logger.error(f"Error during webhook execution: {str(e)}. Falling back to local dispatcher.")
        return fallback_dispatcher(payload.query)
