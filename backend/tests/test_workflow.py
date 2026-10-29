import io, json, os, uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import app as a


@pytest.fixture()
def ctx(monkeypatch):
    pg_url = os.getenv("TEST_DATABASE_URL")
    admin = None
    if pg_url:
        schema = "test_" + uuid.uuid4().hex
        admin = create_engine(pg_url)
        with admin.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine = create_engine(pg_url, connect_args={"options": f"-csearch_path={schema}"})
    else:
        engine = create_engine(
            "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
        )
    factory = sessionmaker(engine, expire_on_commit=False)
    monkeypatch.setattr(a, "engine", engine)
    monkeypatch.setattr(a, "SessionLocal", factory)
    monkeypatch.setenv("REVIEW_MODE", "rules_only")
    a.Base.metadata.create_all(engine)
    with factory() as s:
        for role in ["manager", "creator", "reviewer"]:
            s.add(
                a.User(
                    org="one",
                    email=role + "@test.dev",
                    role=role,
                    password=a.password_hash("safe-test-password"),
                )
            )
        s.add(
            a.User(
                org="other",
                email="other@test.dev",
                role="manager",
                password=a.password_hash("safe-test-password"),
            )
        )
        s.commit()
    with TestClient(a.app) as c:
        headers = {}
        for role in ["manager", "creator", "reviewer", "other"]:
            r = c.post(
                "/api/login",
                json={"email": role + "@test.dev", "password": "safe-test-password"},
            )
            assert r.status_code == 200
            headers[role] = {"Authorization": "Bearer " + r.json()["token"]}
        yield c, headers
    engine.dispose()
    if admin:
        with admin.begin() as connection:
            connection.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        admin.dispose()


def source(c, h, **kw):
    body = {
        "title": "Battery fact",
        "kind": "fact",
        "text": "Up to 12 hours of battery life.",
        "match": "battery life",
        "active": True,
        **kw,
    }
    r = c.post("/api/sources", json=body, headers=h["manager"])
    assert r.status_code == 200, r.text
    return r.json()


def draft(c, h, text="Enjoy up to 12 hours of battery life.", who="creator"):
    b = {
        "title": "Launch",
        "text": text,
        "purpose": "Announce product",
        "audience": "Customers",
        "channel": "social",
    }
    r = c.post("/api/submissions", json=b, headers=h[who])
    assert r.status_code == 200, r.text
    return r.json(), b


def review(c, h, sub):
    return c.post(
        f"/api/revisions/{sub['latest_revision']}/review", json={}, headers=h["creator"]
    )


def request(c, h, sub):
    return c.post(
        f"/api/submissions/{sub['id']}/request-approval",
        json={"revision_id": sub["latest_revision"]},
        headers=h["creator"],
    )


def approve(c, h, sub, **kw):
    return c.post(
        f"/api/submissions/{sub['id']}/approve",
        json={
            "revision_id": sub["latest_revision"],
            "action": "approved",
            "reason": "Verified source and purpose",
            **kw,
        },
        headers=h["reviewer"],
    )


def test_complete_workflow_and_revision_invalidation(ctx):
    c, h = ctx
    source(c, h)
    sub, b = draft(c, h)
    assert review(c, h, sub).json()["status"] == "complete"
    assert request(c, h, sub).status_code == 200
    assert approve(c, h, sub).status_code == 200
    assert (
        c.get("/api/submissions", headers=h["creator"]).json()[0]["status"]
        == "approved"
    )
    r = c.post(
        f"/api/submissions/{sub['id']}/revisions",
        json={**b, "text": "Updated copy"},
        headers=h["creator"],
    )
    assert r.status_code == 200
    assert (
        c.get("/api/submissions", headers=h["creator"]).json()[0]["status"] == "draft"
    )
    assert approve(c, h, sub).status_code == 409


def test_contradiction_and_exception(ctx):
    c, h = ctx
    src = source(c, h)
    sub, _ = draft(c, h, "Enjoy 20 hours of battery life.")
    run = review(c, h, sub).json()
    assert run["findings"][0]["category"] == "contradiction"
    assert run["findings"][0]["source_id"] == src["id"]
    assert request(c, h, sub).status_code == 200
    assert approve(c, h, sub).status_code == 422
    assert (
        approve(
            c, h, sub, exception_reason="Demo exception requiring follow-up"
        ).status_code
        == 200
    )


def test_self_approval_and_tenant_isolation(ctx):
    c, h = ctx
    source(c, h)
    sub, b = draft(c, h, who="manager")
    assert (
        c.post(
            f"/api/submissions/{sub['id']}/approve",
            json={
                "revision_id": sub["latest_revision"],
                "action": "approved",
                "reason": "Self approval",
            },
            headers=h["manager"],
        ).status_code
        == 403
    )
    for path in [
        f"/api/submissions/{sub['id']}",
        f"/api/revisions/{sub['latest_revision']}/review",
    ]:
        r = (
            c.get(path, headers=h["other"])
            if "submissions" in path
            else c.post(path, json={}, headers=h["other"])
        )
        assert r.status_code == 404
    assert c.get("/api/sources", headers=h["other"]).json() == []
    assert (
        c.post(
            "/api/sources",
            json={"title": "X", "kind": "fact", "text": "X"},
            headers=h["creator"],
        ).status_code
        == 403
    )


def test_source_update_revalidation(ctx):
    c, h = ctx
    old = source(c, h)
    sub, _ = draft(c, h)
    review(c, h, sub)
    request(c, h, sub)
    assert approve(c, h, sub).status_code == 200
    source(c, h, supersedes=old["id"], text="Up to 10 hours of battery life.")
    assert (
        c.get("/api/submissions", headers=h["creator"]).json()[0]["status"]
        == "revalidation_required"
    )
    assert request(c, h, sub).status_code == 409
    assert review(c, h, sub).json()["findings"][0]["category"] == "contradiction"


def test_ai_failure_blocks_approval(ctx, monkeypatch):
    c, h = ctx
    source(c, h)
    monkeypatch.setenv("REVIEW_MODE", "ai")
    monkeypatch.delenv("AI_API_KEY", raising=False)
    sub, b = draft(c, h)
    b["ai_consent"] = True
    rev = c.post(
        f"/api/submissions/{sub['id']}/revisions", json=b, headers=h["creator"]
    ).json()
    sub["latest_revision"] = rev["id"]
    result = review(c, h, sub).json()
    assert result["status"] == "incomplete"
    assert result["checks"]["semantic"] == "failed"
    assert request(c, h, sub).status_code == 409


def test_consent_and_source_absence_fail_closed(ctx, monkeypatch):
    c, h = ctx
    sub, _ = draft(c, h)
    assert review(c, h, sub).json()["status"] == "incomplete"
    source(c, h)
    monkeypatch.setenv("REVIEW_MODE", "ai")
    result = review(c, h, sub).json()
    assert result["checks"]["semantic"] == "blocked"
    assert result["status"] == "incomplete"


def test_idempotent_complete_review(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h)
    assert review(c, h, sub).json()["id"] == review(c, h, sub).json()["id"]


def test_expired_source_not_used(ctx):
    c, h = ctx
    source(c, h, valid_until="2000-01-01")
    sub, _ = draft(c, h, "Enjoy 20 hours of battery life.")
    r = review(c, h, sub).json()
    assert r["status"] == "incomplete"
    assert not r["findings"]


def test_comments_and_rejected_findings(ctx):
    c, h = ctx
    source(c, h)
    sub, _ = draft(c, h, "Enjoy 20 hours of battery life.")
    run = review(c, h, sub).json()
    assert (
        c.post(
            "/api/comments",
            json={
                "revision_id": sub["latest_revision"],
                "text": "Check battery qualifier",
            },
            headers=h["reviewer"],
        ).status_code
        == 200
    )
    assert (
        c.post(
            "/api/decisions",
            json={
                "review_id": run["id"],
                "index": 0,
                "action": "rejected",
                "reason": "Please review measurement context",
            },
            headers=h["creator"],
        ).status_code
        == 200
    )
    assert (
        len(c.get("/api/insights", headers=h["manager"]).json()["rejected_findings"])
        == 1
    )


def test_bad_upload_and_word_limit(ctx):
    c, h = ctx
    assert (
        c.post(
            "/api/extract",
            files={"file": ("bad.png", b"not an image", "image/png")},
            headers=h["creator"],
        ).status_code
        == 422
    )
    assert (
        c.post(
            "/api/submissions",
            json={"title": "Too long", "purpose": "Test", "text": "word " * 2001},
            headers=h["creator"],
        ).status_code
        == 422
    )


def test_logout_revokes_session(ctx):
    c, h = ctx
    assert c.post("/api/logout", json={}, headers=h["creator"]).status_code == 200
    assert c.get("/api/me", headers=h["creator"]).status_code == 401


def test_pdf_extraction_rejects_scanned(ctx):
    from pypdf import PdfWriter

    c, h = ctx
    writer = PdfWriter()
    writer.add_blank_page(width=600, height=800)
    buf = io.BytesIO()
    writer.write(buf)
    assert (
        c.post(
            "/api/extract",
            files={"file": ("scan.pdf", buf.getvalue(), "application/pdf")},
            headers=h["creator"],
        ).status_code
        == 422
    )


def test_ai_invalid_citation_fails_closed(ctx, monkeypatch):
    c, h = ctx
    source(c, h)
    sub, b = draft(c, h)
    monkeypatch.setenv("AI_API_KEY", "test")
    monkeypatch.setenv("AI_MODEL", "test")
    monkeypatch.setenv("REVIEW_MODE", "ai")

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "choices": [
                    {
                        "message": {
                            "content": json.dumps(
                                {
                                    "findings": [
                                        {
                                            "category": "tone",
                                            "quote": "Enjoy",
                                            "source_id": 999999,
                                            "evidence": "invented",
                                            "explanation": "test",
                                            "suggestion": "test",
                                            "severity": "low",
                                        }
                                    ]
                                }
                            )
                        }
                    }
                ]
            }

    class FakeClient:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def post(self, *args, **kwargs):
            return Response()

    monkeypatch.setattr(a.httpx, "Client", FakeClient)
    b["ai_consent"] = True
    rev = c.post(
        f"/api/submissions/{sub['id']}/revisions", json=b, headers=h["creator"]
    ).json()
    sub["latest_revision"] = rev["id"]
    assert review(c, h, sub).json()["status"] == "incomplete"


def test_png_dimensions_and_alt_text(ctx, monkeypatch):
    from PIL import Image
    import pytesseract

    monkeypatch.setattr(pytesseract, "image_to_string", lambda *args, **kwargs: "")
    c, h = ctx
    source(c, h, kind="dimension", text="Use 1080 square", match="1080x1080")
    buf = io.BytesIO()
    Image.new("RGB", (100, 100), "white").save(buf, format="PNG")
    att = c.post(
        "/api/extract",
        files={"file": ("creative.png", buf.getvalue(), "image/png")},
        headers=h["creator"],
    ).json()
    sub, b = draft(c, h)
    b["attachment_id"] = att["id"]
    rev = c.post(
        f"/api/submissions/{sub['id']}/revisions", json=b, headers=h["creator"]
    ).json()
    sub["latest_revision"] = rev["id"]
    findings = review(c, h, sub).json()["findings"]
    assert {f["category"] for f in findings} == {"dimensions", "accessibility"}


def test_plain_pdf_extracts_text(ctx):
    from pypdf import PdfWriter
    from pypdf.generic import NameObject, DictionaryObject, DecodedStreamObject

    c, h = ctx
    w = PdfWriter()
    p = w.add_blank_page(width=600, height=800)
    font = DictionaryObject(
        {
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        }
    )
    p[NameObject("/Resources")] = DictionaryObject(
        {NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})}
    )
    stream = DecodedStreamObject()
    stream.set_data(
        b"BT /F1 12 Tf 50 700 Td (Approved battery life is up to 12 hours.) Tj ET"
    )
    p[NameObject("/Contents")] = w._add_object(stream)
    buf = io.BytesIO()
    w.write(buf)
    r = c.post(
        "/api/extract",
        files={"file": ("guide.pdf", buf.getvalue(), "application/pdf")},
        headers=h["manager"],
    )
    assert r.status_code == 200
    assert "12 hours" in r.json()["text"]
