from fastapi.testclient import TestClient

from domain import api
from gpt_api import app

client = TestClient(app=app)


def test_root():
    response = client.get('/')
    assert response.status_code == 200


def test_failed_authentification():
    request = api.Request(
        api_key='',
        prompt='',
        history=[],
    )
    response = client.post('/chat', json=request.model_dump())
    assert response.status_code == 401
