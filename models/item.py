
from db import db

class ItemModel(db.Model):
    __tablename__="items"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    note=db.Column(db.String(300))


    def __init__(self,user_id,note):
        self.user_id=user_id
        self.note=note

    def to_json(self):
        return {'id':self.id,'user_id':self.user_id,'note':self.note}
    
    @classmethod
    def find_by_id(cls,id,user_id):
        return ItemModel.query.filter_by(id=id, user_id=user_id).first()
        
    
    @classmethod
    def find_all(cls,user_id):
        return ItemModel.query.filter_by(user_id=user_id).all()
        
      
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
