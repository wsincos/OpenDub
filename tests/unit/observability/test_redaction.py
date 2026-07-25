from opendub.observability.redaction import redact_details


def test_redaction_removes_sensitive_text_and_credentials() -> None:
    details = {
        "text": "private dialogue",
        "token": "secret",
        "path": "/home/user/project/audio.wav",
        "progress": 0.5,
    }

    redacted = redact_details(details)

    assert redacted == {
        "text": "[redacted]",
        "token": "[redacted]",
        "path": "[redacted]",
        "progress": 0.5,
    }
