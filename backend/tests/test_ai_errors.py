import httpx
import pytest

from app import ai_failure_message


@pytest.mark.parametrize("status", [400, 401, 403, 404, 429, 500])
def test_provider_errors_do_not_expose_secrets_or_content(status):
    request = httpx.Request(
        "POST", "https://provider.test", headers={"Authorization": "secret-key"}
    )
    response = httpx.Response(status, request=request, text="confidential draft")
    error = httpx.HTTPStatusError(
        "secret-key confidential draft", request=request, response=response
    )
    code, message = ai_failure_message(error)
    assert code == f"AI_HTTP_{status}"
    assert "secret-key" not in message
    assert "confidential draft" not in message


def test_timeout_and_invalid_output_are_distinct(monkeypatch):
    monkeypatch.setenv("AI_API_KEY", "private")
    monkeypatch.setenv("AI_MODEL", "test")
    assert ai_failure_message(httpx.ReadTimeout("private"))[0] == "AI_TIMEOUT"
    assert ai_failure_message(ValueError("private"))[0] == "AI_INVALID_RESPONSE"
    monkeypatch.delenv("AI_API_KEY")
    assert ai_failure_message(ValueError("private"))[0] == "AI_CONFIG"
