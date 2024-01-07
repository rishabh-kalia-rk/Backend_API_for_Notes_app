from flask import Flask,request,jsonify
from flask_restful import Api,Resource,reqparse
from flask_jwt import JWT,jwt_required, current_identity
from flask_swagger_ui import get_swaggerui_blueprint
from sqlalchemy import and_
from flask_limiter import Limiter

from db import db
from security import authenticate,identity


from models.item import ItemModel
from models.user import UserModel

# for testing
import pytest


app=Flask(__name__)

import configparser
config= configparser.ConfigParser()
config.read_file(open('.config'))

SECRETE_KEY =config.get('AWS','KEY')

# app.secret_key='jose'
app.secret_key=SECRETE_KEY

jwt=JWT(app,authenticate,identity)




# to configure the postgres

# Get the database connection details
user = config['database']['user']
password = config['database']['password']
host = config['database']['host']
port = config['database']['port']
dbname = config['database']['dbname']

# # Construct the PostgreSQL connection URL
postgres_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# # Configure the PostgreSQL database URI
app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url



# Disable modification tracking as it is deprecated
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False




SWAGGER_URL='/swagger'
API_URL='/static/openapi.json'
SWAGGER_BLUEPRINT=get_swaggerui_blueprint(
	SWAGGER_URL,
	API_URL,
	config={
		'app_name':"list api"
	}

)

# to use swagger
app.register_blueprint(SWAGGER_BLUEPRINT,url_prefix=SWAGGER_URL)
api=Api(app)





# limiter part 

limiter = Limiter(app)
from flask import jsonify
from flask_limiter.util import get_remote_address


limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri="memory://",
)

limiter.init_app(app) 

	


# signup


class UserSignup(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',type=str,required=True)
    parser.add_argument('password',type=str,required=True)
    @limiter.limit("5 per minute")  # Adjust the rate limit as needed
    def post(self):
        data=UserSignup.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":"User already exist"} , 409
        user =UserModel(data['username'],data['password'])
        user.save_to_db()
        return {"message": "user created successfully"} , 200





@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("100 per minute")  # Adjust the rate limit as needed
def generate_token():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    user = authenticate(username, password)
    if user:
        # Manually generate JWT
        token = jwt.jwt_encode_callback(identity=user)
        # token_str = token.decode('utf-8')
        return jsonify({'token': token}),200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401








# to get, to update it and to delete note of particular id.
# Item '/api/notes/<int:id>'

class Item(Resource):
    
    parser= reqparse.RequestParser()
    parser.add_argument('note',
                    type=str,
                    required=True,
                    help="This filed cannot be left empty")


    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def get(self,id):

        # id -  is the id of the note you are searching for
        # user-id - id of user logged in

        user_id = current_identity.id
        note=ItemModel.find_by_id(id,user_id)
        if note:
            return {'reusult':{
                'id':id,
                'user_id':user_id,
                'note':note.note
                }}, 200
        else:
            return {"message":"notes not found"},404


    
    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def put(self,id):

        # id - is the note id you want to update
        # user_d - id of user logged in

        note_data=Item.parser.parse_args()
        if note_data['note']:
            user_id = current_identity.id
    
            item=ItemModel.find_by_id(id,user_id) 

            if item is None:
                return {"Message":"You have no note present of this id to update"}, 404
            else:
                item.note=note_data['note']

            item.save_to_db()
            return {"Updated Note":item.to_json()} , 200
        else:
            return {"message":"delete note if you want to update to empty note"}, 400


    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def delete(self,id):
       
       # id - note id which you want to delete
       # user_id - id of user logged in

       user_id = current_identity.id
       item=ItemModel.find_by_id(id,user_id)
       
       if item:
           item.delete_from_db()
           return {"message":"note deleted"},200
       else:
           return {"message":"note to delete of mentioned id not found"},404
    


# search in user loggedin notes by keyword
# NoteByKeywords - '/api/search/'   
            
class NoteByKeywords(Resource):
    
    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed  
    def get(self):
        # Parse the request arguments
        word= request.args.get('q',default="")
        user_id = current_identity.id
        # Perform a case-insensitive search in the actual database
        
        results = ItemModel.query.filter(ItemModel.user_id == user_id,
    and_(ItemModel.note.ilike(f"%{word}%"))).all()
        if not results:
            return {"Message":"You have no notes that have the word you mentioned"}, 400

        results = [item.to_json() for item in results]
        return {"result":results}, 200


# to get all notes from and add new note to user logged in.
# Note - /api/notes
    
class Note(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('note',type=str,required=True)


    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def get(self):
        user_id = current_identity.id
        notes=ItemModel.find_all(user_id)
        if notes:
            item=[x.to_json() for x in notes]
            return {'item':item}, 200
        else:
            return {"message":"you have no notes"},404
        


    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def post(self):
        dataR=Note.parser.parse_args()
        if not dataR['note']:
            return {"message":"No notes were sent, empty note"},400
        else:
            user_id=current_identity.id
            item=ItemModel(user_id=user_id,note=dataR['note'])
            item.save_to_db()
            
            return {"message":"Note saved","item":item.to_json()}, 200
       


# To share the node among other user.
# NoteShare,'/api/notes/<int:id>/share'
   
class NoteShare(Resource):
           
    @jwt_required()
    @limiter.limit("100 per minute")  # Adjust the rate limit as needed
    def post(self,id):

        # id - id of user to which we want to share note.
        send_to_id=id

        
        user_id = current_identity.id

        # check if user to which we want to share note exist
        check=UserModel.find_by_id(send_to_id)

        notes=ItemModel.find_all(user_id=user_id)
        if not check:
            return {"Message":"User to which you are sending notes does not exist"} , 400
        elif send_to_id==user_id:
            return {"Message": "You are sharing notes with yourself, which you already have"},400
        elif notes:

            for note in notes:
                new_note = ItemModel(user_id=send_to_id, note=note.note)
                ItemModel.save_to_db(new_note)
                mes=f"Notes shared with user id {send_to_id}"
            return {"message":mes},200
        else:
            return {"message":"you have no notes present to share"},404
       







# routes
    
api.add_resource(UserSignup,'/api/auth/signup')
api.add_resource(Note,'/api/notes')
api.add_resource(Item,'/api/notes/<int:id>')
api.add_resource(NoteShare,'/api/notes/<int:id>/share')
api.add_resource(NoteByKeywords,'/api/search')










if __name__=="__main__":
	from db import db
	db.init_app(app)
	app.run(port=5000)

     
    



