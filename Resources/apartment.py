from flask_restx import Resource, fields
from main import api

from Models.apartment import ApartmentModel, apartment_schema, apartments_schema
from  Models.house import houses_schema

apartment_namespace = api.namespace('Apartments', description='This endpoint deals with all operations pertaining apartments')
apartment_model = api.model('APARTMENT', {
    "title" :fields.String(),
    "location" :fields.String(),
    "landlord_id" :fields.Integer()
})


@apartment_namespace.route('')
class ApartmentList(Resource):
    @classmethod
    def get(cls):
        '''Get a list of all apartments under the manager'''
        apartments = ApartmentModel.fetch_all()
        houses = []
        if apartments:
            apartment_list = apartments_schema.dump(apartments)
            apartment_ids = []
            for apartment in apartments:
                apartment_ids.append(apartment.id)
                index = 0
                while index < len(apartment_ids) - 1:
                    apartment = ApartmentModel.fetch_by_id(apartment_ids[index])
                    if apartment:
                        for house in apartment.houses:
                            houses.append(house.house_no)
                            house_dict = {'houses':houses}
                            apartment_list[index].update(house_dict)   
                            print(apartment_list)
                    index += 1

            # houses = []
            #     for house in apartment.houses:
            #             houses.append(house.house_no)
            #             houses_dict = {'houses':houses}
            #             index = 0
            # apartment_list = apartments_schema.dump(apartments)
            # while index < len(apartment_list) - 1:
            #     for apartment in apartment_list:
            #         apartment_list[index].update(houses_dict)
            #         index += 1
            #         print(houses)
            
            
            

            # return apartment_list, 200
        else:
            return {'message':'That apartment does not exists'}, 404

    @classmethod
    @api.expect(apartment_model)
    def post(cls):
        '''Add an apartment to the list of apartments'''
        data = api.payload
        title = data['title']
        apartment = ApartmentModel.fetch_by_title(title)
        if apartment:
            return {'message':'An apartment with that title already exists'}, 400
        else:
            apartment = ApartmentModel(**data)
            apartment.create_record()
            return apartment_schema.dump(apartment), 201


@apartment_namespace.route('/<int:id>')
class Apartment(Resource):
    @classmethod
    def get(cls, id:int):
        '''Get an apartment by its id'''
        apartment = ApartmentModel.fetch_by_id(id)
        if apartment:
            return apartment_schema.dump(apartment), 200
        else:
            return {'message':'That apartment does not exists'}, 404

    @classmethod
    def put(cls, id: int):
        '''edit an endpoint by first querying it by its id'''
        data = api.payload
        apartment = ApartmentModel.fetch_by_id(id)
        if apartment:
            if u'title' in data:
                apartment.title = data['title']
            if u'location' in data:
                apartment.location = data['location']
            if u'lanldlord_id' in data:
                apartment.landlord_id = data['landlord_id']
            return {'updated_apartment':apartment_schema.dump(apartment)}, 200
        else:
            return {'message':'That apartment does not exist'}, 404 

    @classmethod
    def delete(cls, id: int):
        '''Delete an apartment based on its id'''
        apartment = ApartmentModel.fetch_by_id(id)
        if apartment:
            apartment.delete_record()
            return {'message':'apartment succesfully deleted'}, 200
        else:
            return {'message':'That apartment does not exists'}
