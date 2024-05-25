# tests/test_app.py
import pytest
from flask import url_for

def test_register(client, init_db):
    response = client.post(url_for('routes.register'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert b'Login' in response.data
    assert response.status_code == 200

def test_login(client, init_db):
    client.post(url_for('routes.register'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    response = client.post(url_for('routes.login'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert b'Task Management' in response.data
    assert response.status_code == 200

def test_create_task(client, init_db):
    client.post(url_for('routes.register'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    login_response = client.post(url_for('routes.login'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    response = client.post(url_for('routes.tasks_api'), json={
        'name': 'test task',
        'complexity': 'medium',
        'size': 'small',
        'task_type': 'development',
        'notes': 'test notes'
    }, follow_redirects=True)
    assert response.status_code == 201
    assert b'Task created successfully' in response.data

def test_task_details(client, init_db):
    client.post(url_for('routes.register'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    login_response = client.post(url_for('routes.login'), data={
        'username': 'testuser',
        'password': 'testpassword'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    client.post(url_for('routes.tasks_api'), json={
        'name': 'test task',
        'complexity': 'medium',
        'size': 'small',
        'task_type': 'development',
        'notes': 'test notes'
    }, follow_redirects=True)

    response = client.get(url_for('routes.task_details', name='test task'), follow_redirects=True)
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'test task'
    assert 'average_hours' in data
    assert 'confidence_level' in data
    assert 'estimated_range' in data
