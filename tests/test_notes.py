def get_auth_headers(client, name="noteuser", email="noteuser@example.com", password="testpass123"):
    client.post("/user/", json={"name": name, "email": email, "password": password})
    response = client.post("/login", data={"username": email, "password": password})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_note(client):
    headers = get_auth_headers(client)
    response = client.post("/notes/", json={"title": "My note", "body": "Hello"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My note"
    assert "id" in data


def test_get_notes(client):
    headers = get_auth_headers(client)
    client.post("/notes/", json={"title": "My note", "body": "Hello"}, headers=headers)
    response = client.get("/notes/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_note(client):
    headers = get_auth_headers(client)
    created = client.post("/notes/", json={"title": "Old title", "body": "Old body"}, headers=headers)
    note_id = created.json()["id"]

    response = client.put(
        f"/notes/{note_id}",
        json={"title": "New title", "body": "New body"},
        headers=headers,
    )
    assert response.status_code == 202
    assert response.json()["title"] == "New title"


def test_delete_note(client):
    headers = get_auth_headers(client)
    created = client.post("/notes/", json={"title": "To delete", "body": "Bye"}, headers=headers)
    note_id = created.json()["id"]

    response = client.delete(f"/notes/{note_id}", headers=headers)
    assert response.status_code == 204

    # confirm it's really gone
    response = client.get(f"/notes/{note_id}", headers=headers)
    assert response.status_code == 404


def test_create_note_without_token(client):
    response = client.post("/notes/", json={"title": "Sneaky", "body": "No token"})
    assert response.status_code == 401


def test_user_cannot_access_another_users_note(client):
    headers_a = get_auth_headers(client, name="usera", email="usera@example.com")
    headers_b = get_auth_headers(client, name="userb", email="userb@example.com")

    created = client.post("/notes/", json={"title": "A's private note", "body": "Secret"}, headers=headers_a)
    note_id = created.json()["id"]

    # user B tries to read user A's note
    response = client.get(f"/notes/{note_id}", headers=headers_b)
    assert response.status_code == 404

    # user B's own list should be empty
    response = client.get("/notes/", headers=headers_b)
    assert response.json() == []