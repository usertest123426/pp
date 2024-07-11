import pytest
from flask import session
from Auth import app, db, userModel, Appointment, is_slot_available

@pytest.fixture
def client():
    """Fixture for creating a test client for the Flask application."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_register(client):
    # Test registration endpoint
    data = {
        'username': 'testuser',
        'fullName': 'Test User',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    }

    # Test duplicate registration
    response = client.post('/register', json=data)
    assert response.status_code == 401
    assert b'User already exists' in response.data

def test_login(client):
    # Test login endpoint
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    response = client.post('/login', json=data)
    assert response.status_code == 200
    assert session['username'] == 'testuser'  # Check if session is set correctly

    # Test invalid login
    data['password'] = 'wrongpassword'
    response = client.post('/login', json=data)
    assert response.status_code == 401
    assert b'Invalid User or Password' in response.data

def test_appointments(client):
    # Test appointments endpoint (GET)
    response = client.get('/appointments')
    assert response.status_code == 200
    # You can add more assertions based on the expected JSON response

def test_create_appointment(client):
    # Test create appointment endpoint (POST)
    data = {
        'fullName': 'Test Patient',
        'appointmentDate': '2024-07-10',
        'timeSlot': '10:00',
        'wellnessService': 'Yoga Classes'
    }
    response = client.post('/appointments', json=data)
    assert response.status_code == 409
    assert b'Time slot not available' in response.data

def test_update_appointment(client):
    # Test update appointment endpoint (PUT)
    data = {
        'fullName': 'Updated Patient',
        'appointmentDate': '2024-07-10',
        'timeSlot': '11:00',
        'wellnessService': 'Group Fitness'
    }
    response = client.put('/appointments/102', json=data)  # Replace 1 with a valid appointment ID
    assert response.status_code == 404
    assert b'Appointment not found' in response.data

def test_delete_appointment(client):

    # Test delete non-existing appointment
    response = client.delete('/appointments/102')  # Replace 1 with the same or a different ID
    assert response.status_code == 404
    assert b'Appointment not found' in response.data

