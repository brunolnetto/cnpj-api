from starlette.datastructures import Headers

from backend.app.api.middlewares.logs import REDACTED, redact_headers


def test_redact_headers_masks_credentials():
    headers = Headers(
        raw=[
            (b"authorization", b"Bearer secret.jwt.token"),
            (b"cookie", b"session=abc"),
            (b"x-api-key", b"key"),
            (b"user-agent", b"pytest"),
        ]
    )

    redacted = redact_headers(headers)

    assert redacted["authorization"] == REDACTED
    assert redacted["cookie"] == REDACTED
    assert redacted["x-api-key"] == REDACTED
    assert redacted["user-agent"] == "pytest"
    assert "secret.jwt.token" not in str(redacted)


def test_redact_headers_is_case_insensitive():
    redacted = redact_headers({"Authorization": "Bearer x", "Accept": "*/*"})

    assert redacted == {"Authorization": REDACTED, "Accept": "*/*"}
