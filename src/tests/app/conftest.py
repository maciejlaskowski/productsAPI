import pytest
from app import MicroserviceAPI as main

@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    client = main.app.test_client()
    yield client