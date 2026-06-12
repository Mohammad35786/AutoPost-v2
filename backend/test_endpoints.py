from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "connected"}
    print("Health check passed!")

def test_login():
    response = client.post(
        "/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    print("Login passed! Token:", token[:10] + "...")
    
    # Test /me
    me_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "admin@example.com"
    print("Auth/me passed!")

if __name__ == "__main__":
    test_health()
    test_login()
    print("All backend tests passed!")
