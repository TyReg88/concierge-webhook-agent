import pytest
from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_api_health():
    """Test health check root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "Concierge Webhook Agent" in data["service"]

def test_api_get_state(mock_state):
    """Test state retrieval endpoint."""
    response = client.get("/state")
    assert response.status_code == 200
    data = response.json()
    assert "devices" in data
    assert len(data["devices"]) == 4

def test_webhook_fallback_sofa_on(mock_state, monkeypatch):
    """Test sofa light turn on query going to the fallback dispatcher."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    payload = {"query": "Mach das Sofa Licht an"}
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["dispatcher"] == "rule_based_fallback"
    assert "Sofa Licht eingeschaltet" in data["response"]
    
    # Verify the mock state was updated
    state_res = client.get("/state")
    devices = state_res.json()["devices"]
    sofa = next(d for d in devices if d["entity_id"] == "light.ground_livingroom_sofa")
    assert sofa["state"] == "on"

def test_webhook_fallback_sofa_off(mock_state, monkeypatch):
    """Test sofa light turn off query going to the fallback dispatcher."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    # First turn it on
    main.set_device_state("light.ground_livingroom_sofa", "on")
    
    payload = {"query": "Sofa Licht aus bitte"}
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["dispatcher"] == "rule_based_fallback"
    assert "Sofa Licht ausgeschaltet" in data["response"]
    
    # Verify state was updated
    state_res = client.get("/state")
    devices = state_res.json()["devices"]
    sofa = next(d for d in devices if d["entity_id"] == "light.ground_livingroom_sofa")
    assert sofa["state"] == "off"

def test_webhook_fallback_good_morning(mock_state, monkeypatch):
    """Test Good Morning scene query going to the fallback dispatcher."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    payload = {"query": "Guten Morgen! Rollläden aufmachen."}
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["dispatcher"] == "rule_based_fallback"
    assert "alle Rollläden geöffnet" in data["response"]
    
    # Verify covers are open
    state_res = client.get("/state")
    devices = state_res.json()["devices"]
    for d in devices:
        if d["domain"] == "cover":
            assert d["state"] == "open"

def test_webhook_fallback_good_night(mock_state, monkeypatch):
    """Test Good Night scene query going to the fallback dispatcher."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    
    # Ensure they start open
    main.set_device_state("cover.ground_livingroom", "open")
    main.set_device_state("cover.ground_kitchen", "open")
    
    payload = {"query": "Gute Nacht! Alle Rollläden schließen."}
    response = client.post("/webhook", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert data["dispatcher"] == "rule_based_fallback"
    assert "alle Rollläden geschlossen" in data["response"]
    
    # Verify covers are closed
    state_res = client.get("/state")
    devices = state_res.json()["devices"]
    for d in devices:
        if d["domain"] == "cover":
            assert d["state"] == "closed"
