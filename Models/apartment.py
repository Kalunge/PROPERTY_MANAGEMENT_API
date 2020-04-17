from sqlalchemy import func
from typing import List
from main import db, ma
from marshmallow import pre_dump


class ApartmentModel(db.Model):
    __tablename__ = "apartments"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False, unique=True)
    location = db.Column(db.String(), nullable=False)
    houses = db.relationship("HouseModel", backref="apartment", lazy="dynamic")
    landlord_id = db.Column(db.Integer, db.ForeignKey('landlords.id'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    def create_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_record(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def calculate_rent(cls, houses: List):
        """Loop over all the houses in the apartment and return total rent in that apartment"""
        pass

    @classmethod
    def fetch_all(cls) -> "ApartmentModel":
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls, id:int) -> "ApartmentModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_title(cls, title:str) -> "ApartmentModel":
        return cls.query.filter_by(title=title).first()


class ApartmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "location", "created_at", "landlord_id")

    # @pre_dump
    # def pre_dump(self, apartment: ApartmentModel):
    #     apartment.houses = [apartment.houses]
    #     return apartment


apartment_schema = ApartmentSchema()
apartments_schema = ApartmentSchema(many=True)