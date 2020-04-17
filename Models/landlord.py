from sqlalchemy import func
from main import db, ma
from typing import List


class LandlordModel(db.Model):
    __tablename__='landlords'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    phone = db.Column(db.Integer, nullable=False)
    apartments = db.relationship('ApartmentModel', backref='landlord', lazy='dynamic')
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) ->None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def fetch_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls, id:int) -> "LandlordModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_email(cls, email:str) -> "LandlordModel":
        return cls.query.filter_by(email=email).first()

    def claculate_rent(cls):
        pass


class LandlordSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "phone", "created_at")

landlord_schema = LandlordSchema()
landlords_schema = LandlordSchema(many=True)