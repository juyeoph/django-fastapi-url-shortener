from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi_server.main import URL


def test_redirect_to_original_url_success(no_redirect_client: TestClient, db_session: Session):
    test_url = URL(
        original_url="https://www.google.com",
        short_code="testcode",
        click_count=5,
        owner_id=1
    )
    db_session.add(test_url)
    db_session.commit()

    response = no_redirect_client.get(f"/{test_url.short_code}")

    assert response.status_code == 307
    assert response.headers["location"] == test_url.original_url

    updated_url = db_session.query(URL).filter(URL.short_code == "testcode").first()
    assert updated_url is not None
    assert updated_url.click_count == 6


def test_redirect_url_not_found(no_redirect_client: TestClient):
    response = no_redirect_client.get("/nonexistent-code")

    assert response.status_code == 404
    assert response.json() == {"detail": "URL not found"}


def test_favicon_get_request(client: TestClient):
    response = client.get("/favicon.ico")
    assert response.status_code == 204
    assert response.content == b''