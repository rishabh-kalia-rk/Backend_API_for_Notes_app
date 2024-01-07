
from models.user import UserModel



def authenticate(username,password):
    user=UserModel.find_by_username(username)
    #user contain a object,which have attribute like _id, username, password
    if user and user.password==password:
        return user
def identity(payload):
    user_id=payload['identity']
    return UserModel.find_by_id(user_id)