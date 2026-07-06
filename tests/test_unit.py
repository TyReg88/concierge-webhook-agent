import json
import main
from scripts.good_morning import trigger_good_morning
from scripts.good_night import trigger_good_night

def test_get_home_state(mock_state):
    """Test retrieving current simulated state."""
    state = main.get_home_state()
    assert "devices" in state
    assert len(state["devices"]) == 4
    assert state["devices"][0]["entity_id"] == "light.ground_livingroom_sofa"

def test_set_device_state(mock_state):
    """Test modifying device state in the mock database."""
    # Turn on sofa light
    res = main.set_device_state("light.ground_livingroom_sofa", "on")
    assert res == {"status": "success", "entity_id": "light.ground_livingroom_sofa", "state": "on"}
    
    # Verify change is persisted in subsequent read
    state = main.get_home_state()
    sofa_light = next(d for d in state["devices"] if d["entity_id"] == "light.ground_livingroom_sofa")
    assert sofa_light["state"] == "on"

def test_set_device_state_not_found(mock_state):
    """Test setting state of a non-existent device returns error."""
    res = main.set_device_state("light.non_existent_device", "on")
    assert "error" in res
    assert "not found" in res["error"]

def test_trigger_good_morning(mock_state):
    """Test opening all covers in the good morning scene."""
    # Ensure they start closed (defined in conftest.py)
    state_before = main.get_home_state()
    for d in state_before["devices"]:
        if d["domain"] == "cover":
            assert d["state"] == "closed"

    res = trigger_good_morning()
    assert res["status"] == "success"
    assert "opened_covers" in res
    assert len(res["opened_covers"]) == 2
    
    # Verify all covers are now open
    state_after = main.get_home_state()
    for d in state_after["devices"]:
        if d["domain"] == "cover":
            assert d["state"] == "open"

def test_trigger_good_night(mock_state):
    """Test closing all covers in the good night scene."""
    # First, make all covers open
    trigger_good_morning()
    
    res = trigger_good_night()
    assert res["status"] == "success"
    assert "closed_covers" in res
    assert len(res["closed_covers"]) == 2

    # Verify all covers are now closed
    state_after = main.get_home_state()
    for d in state_after["devices"]:
        if d["domain"] == "cover":
            assert d["state"] == "closed"
