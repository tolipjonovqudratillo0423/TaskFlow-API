def test_create_project(client):
    responce = client.post("/projects/", json={
        "name": "Test is going.",
        "description": "1234",
        "status": "active"
    })
    
    assert responce.status_code == 201
    assert "id" in responce.json()