import json
import pytest
from app import app, db  # Assuming you have a create_app function
from models import ItemModel,UserModel





@pytest.fixture(scope="session")
def test_app():
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.init_app(app)
        db.create_all()

    yield app
    
    # Teardown the database after the entire test session
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(test_app):
    client = test_app.test_client()
    return client




@pytest.fixture
def auth_token(client):
    login_data = {'username': 'test_user', 'password': 'test_password'}
    login_response = client.post('/api/auth/login', json=login_data)

    assert login_response.status_code == 200
    assert 'token' in login_response.get_json()

    return login_response.get_json()['token']


@pytest.fixture
def logged_in_user(auth_token):
    return {'token': auth_token}

#-----------------########-------------------------#

def test_signup(client):
    # Test the signup endpoint
    signup_data = {'username': 'test_user', 'password': 'test_password'}
    signup_response = client.post('/api/auth/signup', json=signup_data)

    assert signup_response.status_code == 200
    # Add more assertions for the signup response if needed

    
 

def test_duplicate_signup(client):
    # Test the signup endpoint
    signup_data = {'username': 'test_user', 'password': 'test_password'}
    signup_response = client.post('/api/auth/signup', json=signup_data)

    assert signup_response.status_code == 409

   

def test_login_token(client):
    global auth_token
    test_username = 'test_user'
    test_password = 'test_password'

    with app.app_context():
        db.create_all()  # Create tables if not already created

        test_user = UserModel(test_username, test_password)
        db.session.add(test_user)
        db.session.commit()

    # Prepare login data
    login_data = {
        'username': test_username,
        'password': test_password
    }

    # Send a POST request to the login endpoint
    login_response = client.post('/api/auth/login', json=login_data)

    # Check if the response is as expected
    assert login_response.status_code == 200

    login_response_json=login_response.get_json()

    assert 'token' in login_response_json


def test_wrong_login_token(client):
    test_username = 'test_wrong_user'
    test_password = 'test_wrong_password'


    # Prepare login data
    login_data = {
        'username': test_username,
        'password': test_password
    }

    # Send a POST request to the login endpoint
    login_response = client.post('/api/auth/login', json=login_data)

    # Check if the response is as expected
    assert login_response.status_code == 401

    


#/api/notes
        

def test_post_no_note(client, logged_in_user):
    assert 'token' in logged_in_user

    # Prepare the request data
    note_data = {'note':""}

    # Perform the POST request with the valid token
    response = client.post('/api/notes', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)

    # Assertions
    assert response.status_code == 400
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'No notes were sent, empty note'
    

def test_get_no_notes(client, logged_in_user):
    assert 'token' in logged_in_user

    # Perform the GET request with the valid token
    response = client.get('/api/notes', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    
    # Assertions
    assert response.status_code == 404




def test_post_note(client, logged_in_user):
    assert 'token' in logged_in_user

    # Prepare the request data
    note_data = {'note': 'Test Note Content'}

    # Perform the POST request with the valid token
    response = client.post('/api/notes', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 200
    assert 'message' in json.loads(response.data)
    assert json.loads(response.data)['message'] == 'Note saved'
    # Optionally, you can assert that the data is saved in the database
    with app.app_context():
        user_id =  1
        saved_note = ItemModel.query.filter_by(user_id=user_id, note='Test Note Content').first()
        assert saved_note is not None

# if try to update note to to null

def test_post_empty_note(client, logged_in_user):
    assert 'token' in logged_in_user

    # Prepare the request data
    note_data = {'note': ''}

    # Perform the POST request with the valid token
    response = client.post('/api/notes', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 400



def test_get_notes(client, logged_in_user):
    assert 'token' in logged_in_user

    # Perform the GET request with the valid token
    response = client.get('/api/notes', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    
    # Assertions
    assert response.status_code == 200
    assert 'item' in json.loads(response.data)






# # Item '/api/notes/<int:id>'

def test_get_id_note(client,logged_in_user):
    assert 'token' in logged_in_user

    note_data = {'note': 'Test Note Content'}

    response = client.get('/api/notes/1', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 200
 

def test_get_id_no_note(client,logged_in_user):
    assert 'token' in logged_in_user

    note_data = {'note': 'Test Note Content'}

    # Perform the POST request with the valid token
    response = client.get('/api/notes/10', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 404




def test_put_id_note(client,logged_in_user):
    assert 'token' in logged_in_user

    note_data = {'note': 'updated Test Note Content'}

    # Perform the PUT request with the valid token
    response = client.put('/api/notes/1', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 200
  


def test_put_id_no_note(client,logged_in_user):
    assert 'token' in logged_in_user

    note_data = {'note': 'updated Test Note Content'}

    # Perform the PUT request with the valid token
    response = client.put('/api/notes/10', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 404
  




# NoteByKeywords - '/api/search/'
    
 
def test_search_note(client,logged_in_user):
    assert 'token' in logged_in_user


    # Perform the GET request with the valid token
    response = client.get('/api/search?q=Note', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 200
 



def test_search_no_note(client,logged_in_user):
    assert 'token' in logged_in_user


    # Perform the GET request with the valid token
    response = client.get('/api/search?q=Node', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 400
   



# NoteShare,'/api/notes/<int:id>/share'
    

def test_share_notes(client,logged_in_user):
    assert 'token' in logged_in_user
    signup_data = {'username': 'test_user2', 'password': 'test_password2'}
    signup_response = client.post('/api/auth/signup', json=signup_data)
    assert signup_response.status_code==200


    # Perform the POST request with the valid token
    response = client.post('/api/notes/2/share', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 200


def test_share_no_id_notes(client,logged_in_user):
    assert 'token' in logged_in_user

    # Perform the POST request with the valid token
    response = client.post('/api/notes/18/share', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 400


def test_share_yourself_notes(client,logged_in_user):
    assert 'token' in logged_in_user

    # Perform the POST request with the valid token
    response = client.post('/api/notes/1/share', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 400
  








def test_delete_id_note(client,logged_in_user):
    assert 'token' in logged_in_user
    note_data = {'note': 'updated Test Note Content'}

    # Perform the POST request with the valid token
    response = client.delete('/api/notes/1', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 200



def test_delete_id_no_note(client,logged_in_user):
    assert 'token' in logged_in_user
    note_data = {'note': 'updated Test Note Content'}

    # Perform the POST request with the valid token
    response = client.delete('/api/notes/1', headers={'Authorization': f'JWT {logged_in_user["token"]}'}, json=note_data)
    # Assertions
    assert response.status_code == 404


def test_share_no_notes(client,logged_in_user):
    assert 'token' in logged_in_user

    # Perform the POST request with the valid token
    response = client.post('/api/notes/2/share', headers={'Authorization': f'JWT {logged_in_user["token"]}'})
    # Assertions
    assert response.status_code == 404
