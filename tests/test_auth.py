def test_register_user(client):
    response = client.post("/user/", json={
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data


def test_login_user(client):
    # Register first
    client.post("/user/", json={
        "name": "loginuser",
        "email": "loginuser@example.com",
        "password": "testpass123"
    })

    # Then login
    response = client.post("/login", data={
        "username": "loginuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_register_duplicate_email(client):
    payload = {"name": "Test", "email": "dup@example.com", "password": "secret123"}
    assert client.post("/user/", json=payload).status_code == 201
    response = client.post("/user/", json=payload)
    assert response.status_code == 400

def test_login_wrong_password(client):
    client.post("/user/", json={"name": "Test", "email": "a@example.com", "password": "secret123"})
    response = client.post("/login", data={"username": "a@example.com", "password": "wrong"})
    assert response.status_code == 401