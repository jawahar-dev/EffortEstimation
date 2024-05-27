import pytest
from app import create_app
from app import mongo

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config['SERVER_NAME'] = 'localhost:5000'  # set your server name 
    app.config['APPLICATION_ROOT'] = '/'  # set your application root
    with app.app_context():
        yield app

@pytest.fixture(scope='module')
def client(app):
    with app.app_context():
        with app.test_client() as client:
            yield client


