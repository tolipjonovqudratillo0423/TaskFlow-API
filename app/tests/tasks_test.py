def test_create_task(client, existing_project_and_assignee):
    responce = client.post("/tasks/", json={
        "name": "Test Task!",
        "project_id": existing_project_and_assignee["project"].id,
        "assignee_id": existing_project_and_assignee["assignee"].id
    })
    
    assert responce.status_code == 200
    assert responce.json()["name"] == "Test Task!"
    

def test_get_task_by_id(client, existing_project_and_assignee):
    responce = client.get("/tasks/")
    
    assert responce.status_code == 200