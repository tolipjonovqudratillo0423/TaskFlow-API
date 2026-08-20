# Positive Circumstances

def test_create_task(client, task_testing_essentials):
    response = client.post("/tasks/", json={
        "name": "Test Task!",
        "project_id": task_testing_essentials["project"].id,
        "assignee_id": task_testing_essentials["assignee"].id
    })
    
    assert response.status_code == 201
    assert response.json()["name"] == "Test Task!"
    

def test_get_task_by_id(client, task_testing_essentials):
    response = client.get(f"/tasks/{task_testing_essentials['task'].id}")
    
    assert response.status_code == 200
    

def test_get_all_task_by_owner(client, task_testing_essentials):
    
    response = client.get("/tasks/owner/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2
    
    
def test_get_all_task_by_owner_and_project(client, task_testing_essentials):
    
    response = client.get(f"/projects/{task_testing_essentials['project'].id}/tasks/owner")
    
    assert response.status_code == 200


def test_get_all_task_by_assignee(client, task_testing_essentials_for_assignee):
    
    response = client.get("/tasks/assignee/")
    
    assert response.status_code == 200
    assert response.json()[0]["id"] == 2
    
    
def test_get_all_task_by_assignee_and_project(client, task_testing_essentials_for_assignee):
    
    response = client.get(f"/projects/{task_testing_essentials_for_assignee['project'].id}/tasks/assignee")
    
    assert response.status_code == 200
    

def test_update_task_by_id(client, task_testing_essentials):
    response = client.put(f"/tasks/{task_testing_essentials['task'].id}", json={
        "name": "Update Test!", 
    })
    
    assert response.status_code == 200
    assert response.json()["name"] == "Update Test!"
    

def test_delete_task_by_id(client, task_testing_essentials):
    response = client.delete(f"/tasks/{task_testing_essentials['task'].id}")
    
    assert response.status_code == 200
    assert response.json()["status"] == True


# Negative Circumstances


def test_get_task_by_stranger(client, task_testing_essentials):
    response = client.get(f"/tasks/{task_testing_essentials['second_task'].id}")
    
    assert response.status_code == 403


def test_create_task_with_invalid_data(client, task_testing_essentials):
    response = client.post("/tasks/", json={
        "name": "Test Task!",
        "project_id": 999,
        "assignee_id": 999
    })
    
    assert response.status_code == 422 or response.status_code == 406
    
    
def test_get_all_task_by_owner_and_another_project(client, task_testing_essentials):
    
    response = client.get(f"/projects/{task_testing_essentials['second_project'].id}/tasks/owner")
    
    assert response.status_code == 403
    
    
def test_get_all_task_by_assignee_and_another_project(client, task_testing_essentials_for_assignee):
    
    response = client.get(f"/projects/{task_testing_essentials_for_assignee['second_project'].id}/tasks/assignee")
    
    assert response.status_code == 200
    assert response.json() == {'detail': 'No tasks found!'}
    

def test_update_task_by_stranger(client, task_testing_essentials):
    response = client.put(f"/tasks/{task_testing_essentials['second_task'].id}", json={
        "name": "Update Test!", 
    })
    
    assert response.status_code == 403
    

def test_delete_task_by_stranger(client, task_testing_essentials):
    response = client.delete(f"/tasks/{task_testing_essentials['second_task'].id}")
    
    assert response.status_code == 403
