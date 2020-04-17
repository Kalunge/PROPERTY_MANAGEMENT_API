from sqlalchemy import func
from marshmallow import pre_dump
from main import db, ma
from typing import List

class TenantModel(db.Model):
    __tablename__ = "tenants"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False, unique=True)
    house = db.relationship("HouseModel", backref="tenant", lazy="dynamic")
    # apartment_id = db.Column(db.Integer, ForeignKey('apartments.id'), nullable=False)
    # landlord_id = db.Column(Integer, db.ForeignKey('landlords.id'), nullable=False)
    phone_number = db.Column(db.Integer, unique=True, nullable=False)
    identity_number = db.Column(db.Integer, unique=True, nullable=False)
    employed = db.Column(db.Boolean, default=False, nullable=False)
    deposit = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    next_of_kin = db.Column(db.String(), nullable=False)
    security_charges = db.Column(db.Float)
    garbage_depost = db.Column(db.Float)

    def create_record(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_record(self) ->None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_all(cls) -> List:
        return cls.query.all()

    @classmethod
    def fetch_by_id(cls, id: int) -> "TenantModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def fetch_by_email(cls, email: str) -> "TenantModel":
        return cls.query.filter_by(email=email).first()


class TenantSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "full_name",
            "email",
            # "house",
            "apartment_id",
            "landlord_id",
            "phone_number",
            "identity_number",
            "employed",
            "deposit",
            "created_at",
            "next_of_kin",
            "security_charges",
            "garbage_depost",
        )

        # @pre_dump
        # def pre_dump(self, tenant: TenantModel):
        #     tenant.house = [tenant.house]
        #     return tenant


tenant_schema = TenantSchema()
tenants_schema = TenantSchema(many=True)
