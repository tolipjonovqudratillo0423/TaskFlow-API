
# Positive Circumstances

def test_create_project(client):
    response = client.post("/projects/", json={
        "name": "Test is going.",
        "description": "1234",
        "status": "active"
    })
    
    assert response.status_code == 201
    assert "id" in response.json()


def test_get_all_project(client):
    response = client.get("/projects/")
    
    assert response.status_code == 200
    

def test_get_project_by_id(client, existing_project):
    response = client.get(f"/projects/{existing_project['project'].id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project!"
    

def test_update_project_by_id(client, existing_project):
    response = client.put(f"/projects/{existing_project['project'].id}", json={
        "name": "Update Test!", 
        "description": "Just Test is going!",
        "status": "archived"
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "Update Test!"
    

def test_delete_project_by_id(client, existing_project):
    response = client.delete(f"/projects/{existing_project['project'].id}")
    
    assert response.status_code == 200
    assert response.json()["status"] == True
    
# Negative Circumstances


def test_create_project_with_invalid_data(client):
    response = client.post("/projects/", json={
        "name": 21,
        "description": "1234",
        "status": "active"
    })
    
    assert response.status_code == 422


def test_get_project_by_stranger(client, existing_project):
    response = client.get(f"/projects/{existing_project['second_project'].id}")
    
    assert response.status_code == 404
    

def test_update_project_by_stranger(client, existing_project):
    response = client.put(f"/projects/{existing_project['second_project'].id}", json={
        "name": "Update Test!", 
        "description": "Just Test is going!",
        "status": "archived"
    })
    
    assert response.status_code == 404

    

def test_delete_project_by_stranger(client, existing_project):
    response = client.delete(f"/projects/{existing_project['second_project'].id}")
    
    assert response.status_code == 404

 