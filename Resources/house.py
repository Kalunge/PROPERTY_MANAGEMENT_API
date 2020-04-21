from flask_restx import Resource, fields
from Models.house import HouseModel, houses_schema, house_schema
from main import api
from Models.tenant import TenantModel
from Models.apartment import ApartmentModel

house_namesapce = api.namespace(
    "Houses", description="deals with all operations pertaining houses"
)

house_model = api.model(
    "HOUSE",
    {
        "number_of_bedrooms": fields.Integer(),
        "rent": fields.Float(),
        "house_no": fields.String(),
        "occupied": fields.Boolean(),
        "tenant_id": fields.Integer(),
        "apartment_id" :fields.Integer()
        # "landlord_id" :fields.Integer()
    },
)


@house_namesapce.route("")
class HouseList(Resource):
    @classmethod
    def get(cls):
        """Get a list of all houses in an apartment"""
        houses = HouseModel.fetch_all()
        if houses:
            house_list = houses_schema.dump(houses)
            index = 0
            while index < len(house_list) - 1:

                    #GET TENANT NAME
                tenant_id = house_list[index]['tenant_id']
                tenant_name = TenantModel.fetch_by_id(tenant_id).full_name
                tenant_dict = {'Tenant' :tenant_name}
                house_dict_list = houses_schema.dump(houses)


                for each_dict in house_dict_list:
                    each_dict.update(tenant_dict)

                    #GET APARTMENT NAME AS BLOCK
                apartment_id = house_list[index]['apartment_id']
                apartment_name = ApartmentModel.fetch_by_id(apartment_id).title
                apartment_dict = {'Block': apartment_name}

                # index += 1
                index += 1
                # tenant_id += 1
                # apartment_id += 1

            # house_dict_list = houses_schema.dump(houses)
            
            #     print(each_dict)
            #     each_dict.update(apartment_dict) 


            return house_dict_list, 200
        else:
            return {"message": "THere are no houses to display at the moment"}, 404

    @classmethod
    @api.expect(house_model)
    def post(cls):
        """Add a house to the list of houses in an apartment"""
        data = api.payload
        house_no = data["house_no"]
        house = HouseModel.fetch_by_house_no(house_no)
        if house:
            return {"message": "THat house already exists in the system"}, 400
        else:
            house = HouseModel(**data)
            house.add_record()
            tenant = TenantModel.fetch_by_id(house.tenant_id)
            if tenant:
                tenant_dict = {'tenant':tenant.full_name}
                house_dict = house_schema.dump(house)
                apartment = ApartmentModel.fetch_by_id(house.apartment_id)
                apartment_dict = {'Block':apartment.title}
                house_dict.update(tenant_dict)
                house_dict.update(apartment_dict)
                return house_dict, 201
            else:
                house.delete_record()
                return {'message':'Please add a valid tenant'}, 400


@house_namesapce.route("/<int:id>")
class House(Resource):
    @classmethod
    def get(cls, id:int):
        """Get a house based on its id"""
        house = HouseModel.fetch_by_id(id)
        if house:
                #GET TENANT NAME
            tenant = TenantModel.fetch_by_id(house.tenant_id)
            house_dict = house_schema.dump(house)
            tenant_dict = {"tenant": tenant.full_name}
            house_dict.update(tenant_dict)
                #GET BLOCK NAME
            block = ApartmentModel.fetch_by_id(house.apartment_id).title
            block_dict = {'Block': block}
            house_dict.update(block_dict)

            return house_dict, 200
        else:
            return {"message": "That house does not exist"}, 404

    @classmethod
    @api.expect(house_model)
    def put(cls, id:int):
        """Edit a house by first querying it by its id"""
        data = api.payload
        house = HouseModel.fetch_by_id(id)
        if house:
            if u"number_of_bedrooms" in data:
                house.number_of_bedrooms = data["number_of_bedrooms"]
            if u"rent" in data:
                house.rent = data["rent"]
            if u"house_no" in data:
                house.house_no = data["house_no"]
            if u"tenant_id" in data:
                house.tenant_id = data["tenant_id"]
            house.add_record()
            house_dict = house_schema.dump(house)
                #Get Tenant name 
            tenant_name = TenantModel.fetch_by_id(house.tenant_id).full_name
            tenant_dict = {'Tenant': tenant_name}
            house_dict.update(tenant_dict)
                #Get Block Name
            block_name = ApartmentModel.fetch_by_id(house.apartment_id).title
            block = {'Block':block_name}
            house_dict.update(block)

            return (
                {
                    "message": "House successfully updated",
                    "updated_house": house_dict,
                },
                200,
            )
        else:
            return {"message": "The house you are trying to edit does not exists"}, 404

    @classmethod
    def delete(cls, id:int):
        """Delet a house based on its id"""  # Why would I need to delete a house anywa??
        house = HouseModel.fetch_by_id(id)
        if house:
            house.delete_record()
            return {"message": "House deleted successfully"}, 200
        else:
            return (
                {"message": "The house you are trying to delete does not exists"},
                404,
            )