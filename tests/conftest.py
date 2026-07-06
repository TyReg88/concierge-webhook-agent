import pytest
import json
import os
import main
import scripts.good_morning
import scripts.good_night

@pytest.fixture
def mock_state(tmp_path):
    """
    Fixture that creates a temporary mock state JSON file and patches all
    modules to use this file during tests, preventing changes to the active db.
    """
    test_state_file = tmp_path / "test_mock_state.json"
    
    # Standard initial data for tests
    initial_data = {
        "devices": [
            {
                "entity_id": "light.ground_livingroom_sofa",
                "friendly_name": "Sofa Licht",
                "state": "off",
                "domain": "light",
                "floor": "ground"
            },
            {
                "entity_id": "light.ground_kitchen",
                "friendly_name": "Küche Licht",
                "state": "off",
                "domain": "light",
                "floor": "ground"
            },
            {
                "entity_id": "cover.ground_livingroom",
                "friendly_name": "Wohnzimmer Rollladen",
                "state": "closed",
                "domain": "cover",
                "floor": "ground"
            },
            {
                "entity_id": "cover.ground_kitchen",
                "friendly_name": "Küche Rollladen",
                "state": "closed",
                "domain": "cover",
                "floor": "ground"
            }
        ]
    }
    
    # Write the initial test state
    test_state_file.write_text(json.dumps(initial_data, indent=4), encoding="utf-8")
    
    # Store original values
    orig_main_path = main.MOCK_STATE_PATH
    orig_gm_path = scripts.good_morning.MOCK_STATE_PATH
    orig_gn_path = scripts.good_night.MOCK_STATE_PATH
    
    # Patch modules
    main.MOCK_STATE_PATH = str(test_state_file)
    scripts.good_morning.MOCK_STATE_PATH = str(test_state_file)
    scripts.good_night.MOCK_STATE_PATH = str(test_state_file)
    
    yield test_state_file
    
    # Restore original values
    main.MOCK_STATE_PATH = orig_main_path
    scripts.good_morning.MOCK_STATE_PATH = orig_gm_path
    scripts.good_night.MOCK_STATE_PATH = orig_gn_path
