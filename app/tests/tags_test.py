def test_get_all_tags(client):
    response = client.get("/tags/")
    assert response.status_status_code == 200


def test_get_tag_by_id(client, tag_essentials):
    response = client.get(f"/tags/{tag_essentials["tag"].id}")
    assert response.status_code == 200
        