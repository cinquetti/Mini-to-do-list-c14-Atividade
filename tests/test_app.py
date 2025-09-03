import sys
import os

# Adiciona a pasta raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app
from app.database import db
from app.models import Task



# ---------- FIXTURES ----------
@pytest.fixture
def app():
    """Configura um app Flask para testes (banco em memória)."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Cria um cliente de testes para simular requisições HTTP."""
    return app.test_client()


# ---------- TESTES POSITIVOS ----------
def test_homepage_status_code(client):
    response = client.get("")
    assert response.status_code == 200


def test_add_task(client, app):
    response = client.post("/add", data={"title": "Tarefa 1"}, follow_redirects=True)
    assert b"Tarefa 1" in response.data


def test_toggle_task(client, app):
    with app.app_context():
        task = Task(title="Tarefa toggle")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    client.get(f"/toggle/{task_id}", follow_redirects=True)
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.done is True


def test_delete_task(client, app):
    with app.app_context():
        task = Task(title="Tarefa delete")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    client.get(f"/delete/{task_id}", follow_redirects=True)
    with app.app_context():
        deleted_task = Task.query.get(task_id)
        assert deleted_task is None


def test_add_multiple_tasks(client, app):
    client.post("/add", data={"title": "Task A"})
    client.post("/add", data={"title": "Task B"})
    with app.app_context():
        tasks = Task.query.all()
        assert len(tasks) == 2


def test_task_persists_in_db(app, client):
    client.post("/add", data={"title": "Persistência"})
    with app.app_context():
        task = Task.query.filter_by(title="Persistência").first()
        assert task is not None


def test_template_renders_index(client):
    response = client.get("/")
    assert b"Suas tarefas" in response.data


def test_template_renders_add_page(client):
    response = client.get("/add")
    assert b"Adicionar Tarefa" in response.data


def test_task_done_toggle_twice(client, app):
    with app.app_context():
        task = Task(title="Duplo toggle")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    client.get(f"/toggle/{task_id}")
    client.get(f"/toggle/{task_id}")
    with app.app_context():
        updated_task = Task.query.get(task_id)
        assert updated_task.done is False


def test_delete_task_redirects(client, app):
    with app.app_context():
        task = Task(title="Redirect delete")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.get(f"/delete/{task_id}")
    assert response.status_code == 302  # redireciona para homepage


# ---------- TESTES NEGATIVOS ----------
def test_add_task_empty_title(client, app):
    response = client.post("/add", data={"title": "   "}, follow_redirects=True)
    assert b"Nenhuma tarefa encontrada" in response.data


def test_toggle_invalid_task(client):
    response = client.get("/toggle/999", follow_redirects=True)
    assert response.status_code == 404


def test_delete_invalid_task(client):
    response = client.get("/delete/999", follow_redirects=True)
    assert response.status_code == 404


def test_homepage_without_tasks(client):
    response = client.get("/")
    assert b"Nenhuma tarefa encontrada" in response.data


def test_sql_injection_title(client, app):
    malicious = "'; DROP TABLE tasks; --"
    client.post("/add", data={"title": malicious})
    with app.app_context():
        task = Task.query.filter_by(title=malicious).first()
        assert task is not None  # apenas salva como string


def test_long_title(client, app):
    long_title = "A" * 500  # maior que 200 caracteres
    client.post("/add", data={"title": long_title})
    with app.app_context():
        task = Task.query.filter_by(title=long_title[:200]).first()
        assert task is None  # deve falhar no limite de coluna


def test_toggle_task_invalid_method(client, app):
    with app.app_context():
        task = Task(title="Método inválido")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f"/toggle/{task_id}")
    assert response.status_code in (405, 500)  # método errado


def test_delete_task_invalid_method(client, app):
    with app.app_context():
        task = Task(title="Delete errado")
        db.session.add(task)
        db.session.commit()
        task_id = task.id

    response = client.post(f"/delete/{task_id}")
    assert response.status_code in (405, 500)


def test_access_invalid_route(client):
    response = client.get("/rota_inexistente")
    assert response.status_code == 404
