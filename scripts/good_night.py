import json
import os

MOCK_STATE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "mock_state.json"))

def trigger_good_night() -> dict:
    """
    Closes all covers in the simulated home environment.
    Returns a dictionary summarizing the actions taken.
    """
    try:
        with open(MOCK_STATE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"error": f"Could not read mock state file at {MOCK_STATE_PATH}"}

    updated_entities = []
    for device in data.get("devices", []):
        if device.get("domain") == "cover" and device.get("state") != "closed":
            device["state"] = "closed"
            updated_entities.append(device.get("entity_id"))

    if updated_entities:
        try:
            with open(MOCK_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            return {"error": f"Failed to save updated state: {str(e)}"}

    return {
        "status": "success",
        "scene": "good_night",
        "closed_covers": updated_entities
    }

if __name__ == "__main__":
    result = trigger_good_night()
    print(json.dumps(result, indent=2))
