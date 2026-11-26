import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient

from backend.app.api.middlewares.logs import REDACTED, RequestAuditMiddleware


@pytest.fixture
def records():
    return []


def _client(persist) -> TestClient:
    app = FastAPI()
    app.add_middleware(RequestAuditMiddleware, persist=persist)

    @app.get("/json")
    def json_route():
        return {"hello": "world"}

    @app.get("/stream")
    def stream_route():
        return StreamingResponse(iter([b"abc", b"defg"]), media_type="text/plain")

    @app.get("/boom")
    def boom_route():
        raise RuntimeError("boom")

    return TestClient(app, raise_server_exceptions=False)


def test_writes_one_record_per_request(records):
    client = _client(records.append)

    response = client.get(
        "/json", headers={"Authorization": "Bearer secret", "User-Agent": "pytest"}
    )

    assert response.status_code == 200
    assert len(records) == 1

    record = records[0]
    assert record["relo_method"] == "GET"
    assert record["relo_status_code"] == 200
    assert record["relo_response_size"] == len(response.content)
    assert record["relo_device_info"] == "pytest"
    assert record["relo_headers"]["authorization"] == REDACTED
    assert record["relo_request_duration_seconds"] >= 0


def test_streaming_response_size_is_counted_without_buffering(records):
    client = _client(records.append)

    response = client.get("/stream")

    assert response.text == "abcdefg"
    assert records[0]["relo_response_size"] == 7


def test_unhandled_error_is_recorded_as_500(records):
    client = _client(records.append)

    response = client.get("/boom")

    assert response.status_code == 500
    assert records[0]["relo_status_code"] == 500


def test_failing_audit_write_does_not_break_the_request():
    def failing_persist(_log_data):
        raise ConnectionError("audit database is down")

    response = _client(failing_persist).get("/json")

    assert response.status_code == 200
    assert response.json() == {"hello": "world"}
