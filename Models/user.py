from main import db, ma

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def fetch_all(cls):
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls, id:int):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def fetch_by_email(cls, email:str):
        return cls.query.filter_by(email=email).first()
    


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "full_name", "email")

user_schema = UserSchema()
users_schema = UserSchema(many=True)