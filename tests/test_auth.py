def test_register_user(client):
    response = client.post("/user/", json={
        "name": "testuser",
        "email": "testuser@example.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
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