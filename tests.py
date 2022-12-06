import json
from datetime import datetime

import pytest

from db import *
from main import create_app
@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_log_in_admin(client):
    admin ={
        "user_name": "admin",
        "password_hash": "password"
    }

    response = client.post("/api/v1/admin",
                           json=admin,
                           headers={"Content-Type": "application/json"})

    res = json.loads(response.data.decode('utf-8'))

    assert res["token"] != None
    global token
    token = res["token"]

def test_insert_book(client):
    book = {
          "name" : "AI full course 4",
#         "year" : "2004-05-05",
#         "language" : "English",
#         "id_genre" : 1,
#         "author_id" : 1,
#         "status": "available",
#         "price": 1000,
#         "description" : "A book",
#         "photo_url" : "http://aaa"
    }
    response = client.post('/book',
                            json=book,
                            headers={"Content-Type": "application/json", "token": token})

    assert response.status_code == 200

def test_update_book(client):
    updates = {
        "language" : "Hindi"
    }

    response = client.put('/book',
                            json=updates,
                            headers={"Content-Type": "application/json", "token": token})

    assert response.status_code == 200

def test_get_books(client):
    response = client.get('/books')
    res = json.loads(response.data.decode('utf-8'))

    assert type(res) is list
    assert response.status_code == 200

def test_delete_movie(client):
    response = client.delete(f'book/{id}',
                                headers={"token": token})

    assert response.status_code == 200
