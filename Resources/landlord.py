from flask_restx import Resource, fields
from Models.landlord import LandlordModel, landlords_schema, landlord_schema
from main import api

landlord_namespace = api.namespace('Landlords', description='This Endpoint deals with all operations dealing with landlords')
landlord_model = api.model('LANDLORD', {
    "name" :fields.String(),
    "email" :fields.String(),
    "phone" :fields.Integer()
})


@landlord_namespace.route('')
class LandlordList(Resource):
    @classmethod
    def get(cls):
        '''Get a list of landlords in the system'''
        landlords = LandlordModel.fetch_all()
        if landlords:
            return landlords_schema.dump(landlords)
        else:
            return {'message':'there are no landlords in the system'}, 404

    @classmethod
    @api.expect(landlord_model)
    def post(cls):
        '''Add a landlord to the list of landlords in the system'''
        data = api.payload
        email = data['email']
        landlord = LandlordModel.fetch_by_email(email)
        if landlord:
            return {'message':'a landlord by that email already exists'}, 400
        else:
            landlord = LandlordModel(**data)
            landlord.save_to_db()
            return landlord_schema.dump(landlord)


@landlord_namespace.route('/<int:id>')
class LandLord(Resource):
    @classmethod
    def get(cls, id:int):
        '''Get a specific landlord based on their id'''
        landlord = LandlordModel.fetch_by_id(id)
        if landlord:
            return landlord_schema.dump(landlord)
        else:
            return {'message':'That landlord does not exists'}, 404

    @classmethod
    def delete(cls, id:int):
        '''DElete a certain landlord based on their id'''
        landlord = LandlordModel.fetch_by_id(id)
        if landlord:
            landlord.delete_from_db()
            return {'message':'Landlord delted succesfully'}, 200
        else:
            return {'message':'landlord doe not exists'}, 404

    @classmethod
    @api.expect(landlord_model)
    def put(cls, id:int):
        '''EDit a certain landlord based on their id'''
        data = api.payload
        landlord = LandlordModel.fetch_by_id(id)
        if landlord:
            if "name" in data:
                landlord.name = data['name']
            if "email" in data:
                landlord.email = data['email']
            if u'phone' in data:
                landlord.phone = data['phone']
            return landlord_schema.dump(landlord)
        else:
            return {'message':'That landlord does not exists'}, 404