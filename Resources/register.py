from main import api
from flask_restx import Resource, fields

register_namespace = api.namespace('Register', description='This endpoint deals with registering new users to the system')
register_model = api.model('USER', {
    "full_name" :fields.String(),
    "email" :fields.String()
})

@register_namespace.route('')
class UserList(Resource):
    @classmethod
    def get(cls):
        '''Get a list of managers in the system'''
        pass

    @classmethod
    def post(cls):
        '''Add a user to the system'''
        pass

@register_namespace.route('/<int:id>')
class User(Resource):
    @classmethod
    def get(cls, id:int):
        '''Get a user based on their id'''
        pass

    @classmethod
    def delte(cls, id:int):
        '''Delete a user based on their id'''
        pass

    @classmethod
    def update(cls, id):
        '''Edit users details by querying them by their id'''
        pass