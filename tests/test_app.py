import pytest
from flask import url_for

def test_register(client):
    response = client.post(url_for('routes.register'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    assert b'Login' in response.data
    assert response.status_code == 200

def test_login(client):
    client.post(url_for('routes.register'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    response = client.post(url_for('routes.login'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200

def test_create_task(client):
    client.post(url_for('routes.register'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    response = client.post(url_for('routes.login'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    assert response.status_code == 200

    response = client.post(url_for('routes.tasks_api'), json={
        'name': 'task',
        'complexity': 'medium',
        'size': 'small',
        'task_type': 'development',
        'notes': 'notes'
    }, follow_redirects=True)
    assert b'Task created successfully' in response.data

def test_task_estimation(client):
    client.post(url_for('routes.register'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    login_response = client.post(url_for('routes.login'), data={
        'username': 'user',
        'password': 'password'
    }, follow_redirects=True)
    assert login_response.status_code == 200

    client.post(url_for('routes.tasks_api'), json={
        'name': 'task',
        'complexity': 'medium',
        'size': 'small',
        'task_type': 'development',
        'notes': 'notes'
    }, follow_redirects=True)

    response = client.get(url_for('routes.task_estimation', name='task'), follow_redirects=True)
    assert response.status_code == 200
    out = response.get_json()
    assert out['name'] == 'task'
    assert 'average_hours' in out
    assert 'confidence_level' in out
    assert 'estimated_range' in out
