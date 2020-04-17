from main import db, ma
from sqlalchemy import func
from typing import List
from Models.tenant import TenantModel


class HouseModel(db.Model):
    __tablename_ = "houses"

    id = db.Column(db.Integer, primary_key=True)
    number_of_bedrooms = db.Column(db.Integer, nullable=False)
    rent = db.Column(db.Float, nullable=False)
    house_no = db.Column(db.String(), nullable=False, unique=True)
    occupied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    tenant_id = db.Column(db.Integer, db.ForeignKey("tenants.id"))
    apartment_id = db.Column(db.Integer, db.ForeignKey("apartments.id"))
    # landlord_id = db.Column(db.Integer, db.ForeignKey("lanlords.id"))

    def add_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_record(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def delete_all(cls):
    #     cls.query().delete()
           

    @classmethod
    def fetch_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls, id:int) -> "HouseModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_house_no(cls, house_no:str) -> "HouseModel":
        return cls.query.filter_by(house_no=house_no).first()

    @classmethod
    def get_tenant_id(cls, id:int) -> int:
        return cls.query.filter_by(id=id).first().tenant_id


class HouseSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "number_of_bedrooms",
            "rent",
            "house_no",
            "occupied",
            "created_at",
            "tenant_id",
            "landlord_id",
            "apartment_id",
        )


house_schema = HouseSchema()
houses_schema = HouseSchema(many=True)
