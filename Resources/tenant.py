from Models.tenant import TenantModel, tenants_schema, tenant_schema
from flask_restx import Resource, fields
from main import api

tenant_namespace = api.namespace(
    "Tenants", description="This Endpoint deals with all operations pertaining tenants"
)

tenant_model = api.model(
    "TENANT",
    {
        "full_name": fields.String(),
        "email": fields.String(),
        # "apartment_id": fields.Integer(),
        # "landlord_id" :fields.Integer(),
        "phone_number": fields.Integer(),
        "identity_number": fields.Integer(),
        "employed": fields.Boolean(),
        "deposit": fields.Float(),
        "next_of_kin": fields.String(),
        "security_charges": fields.Float(),
        "garbage_depost": fields.Float(),
    },
)


@tenant_namespace.route("")
class TenantsList(Resource):
    @classmethod
    def get(cls):
        """Get a list of all tenants in a certain apartment"""
        tenants = TenantModel.fetch_all()
        if tenants:
            return tenants_schema.dump(tenants), 200
        else:
            return {"message": "There are no tenants in this apartment"}, 404

    @classmethod
    @api.expect(tenant_model)
    def post(cls):
        """Add a tenant to a certain apartment"""
        data = api.payload
        email = data["email"]
        tenant = TenantModel.fetch_by_email(email)
        if tenant:
            return {"message": "A tenant by that email already exists"}, 400
        else:
            tenant = TenantModel(**data)
            tenant.create_record()
            return tenant_schema.dump(tenant), 201


@tenant_namespace.route("/<int:id>")
class Tenant(Resource):
    @classmethod
    def get(cls, id:int):
        """Get a tenant by their id"""
        tenant = TenantModel.fetch_by_id(id)
        if tenant:
            houses = tenant.house
            tenant_dict = tenant_schema.dump(tenant)
            house = [house.house_no for house in houses]
            tenant_dict.update({"house": house[0]})

            return tenant_dict, 200
        else:
            return {"message": "That tenant does not exists"}, 404

    @classmethod
    def put(cls, id:int):
        """Edit tenant's details after querying them by their id"""
        data = api.payload
        tenant = TenantModel.fetch_by_id(id)
        if tenant:
            if u"full_name" in data:
                tenant.full_name = data["full_name"]
            if u"phone_number" in data:
                tenant.phone_number = data["phone_number"]
            if u"phone_number" in data:
                tenant.phone_number = data["phone_number"]
            return {"message": "Tenant details updated succesfully"}, 200
        else:
            return {"message": "That could not be found"}

    @classmethod
    def delete(cls, id:int):
        """delete a tenant by their id"""
        tenant = TenantModel.fetch_by_id(id)
        if tenant:
            tenant.delete_record()
            return {"message": "Tenant deleted successfully"}, 200
        else:
            return {"message": "That tenant does not exists"}, 404
