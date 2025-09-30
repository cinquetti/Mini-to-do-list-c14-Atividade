import sys
import os
from types import SimpleNamespace
from unittest.mock import MagicMock, patch
import pytest

# garante que a raiz do projeto esteja no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from app.database import db
from app.models import Task


# ---------- FIXTURES ----------
@pytest.fixture
def app():
    """Configura o app Flask para testes (banco em memória)."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cliente de testes HTTP."""
    return app.test_client()


# ---------- TESTES USANDO MOCKS ----------

def test_index_renders_tasks_from_query(client):
    mock_task = SimpleNamespace(id=7, title="FromQuery", done=False)
    with patch("app.models.Task.query") as mock_query:
        mock_query.all = MagicMock(return_value=[mock_task])
        resp = client.get("/")
        assert b"FromQuery" in resp.data

def test_toggle_nonexistent_raises_404(client):
    from werkzeug.exceptions import NotFound
    with patch("app.models.Task.query") as mock_query:
        mock_query.get_or_404 = MagicMock(side_effect=NotFound())
        resp = client.get("/toggle/999")
        assert resp.status_code == 404


def test_delete_nonexistent_raises_404(client):
    from werkzeug.exceptions import NotFound
    with patch("app.models.Task.query") as mock_query:
        mock_query.get_or_404 = MagicMock(side_effect=NotFound())
        resp = client.get("/delete/999")
        assert resp.status_code == 404


def test_sql_injection_stored_as_string(client, app):
    malicious = "'; DROP TABLE task; --"
    client.post("/add", data={"title": malicious}, follow_redirects=True)
    with app.app_context():
        task = Task.query.filter_by(title=malicious).first()
        assert task is not None  # apenas salva como string
