from sqlalchemy import text


def test_register_login_refresh_logout_flow(client):
    register_response = client.post(
        "/api/auth/register",
        json={
            "email": "student@example.com",
            "password": "secret123",
            "full_name": "Student Example",
            "subject": "precalculo",
        },
    )
    assert register_response.status_code == 201

    register_data = register_response.json()
    assert register_data["user"]["email"] == "student@example.com"
    assert register_data["access_token"]
    assert register_data["refresh_token"]
    assert "token_type" not in register_data
    assert "is_active" not in register_data["user"]
    assert "created_at" not in register_data["user"]
    assert "updated_at" not in register_data["user"]

    me_response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {register_data['access_token']}"},
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "student@example.com"

    login_response = client.post(
        "/api/auth/login",
        json={"email": "student@example.com", "password": "secret123"},
    )
    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]
    refresh_response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert refresh_response.status_code == 200
    assert refresh_response.json()["refresh_token"] != refresh_token

    logout_response = client.post(
        "/api/auth/logout",
        json={"refresh_token": refresh_response.json()["refresh_token"]},
    )
    assert logout_response.status_code == 204

    refresh_after_logout_response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_response.json()["refresh_token"]},
    )
    assert refresh_after_logout_response.status_code == 401


def test_register_rejects_password_longer_than_bcrypt_limit(client):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "student2@example.com",
            "password": "a" * 73,
            "full_name": "Student Example",
            "subject": "precalculo",
        },
    )

    assert response.status_code == 422


def test_register_persists_lowercase_enum_values(client, db_session):
    response = client.post(
        "/api/auth/register",
        json={
            "email": "student3@example.com",
            "password": "secret123",
            "full_name": "Student Example",
            "subject": "preuniversitario",
        },
    )

    assert response.status_code == 201

    row = db_session.execute(
        text(
            "SELECT subject, role "
            "FROM users WHERE email = :email"
        ),
        {"email": "student3@example.com"},
    ).fetchone()

    assert row is not None
    assert row[0] == "preuniversitario"
    assert row[1] == "student"
