from flask_restful import Resource, reqparse
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from ..models import KeyValueModel, UserModel

parser = reqparse.RequestParser()


class SetItem(Resource):
    parser.add_argument('key', help = 'This field cannot be blank', required = True)
    parser.add_argument('value', help = 'This field cannot be blank', required = True)

    @jwt_required
    def post(self):
        data = parser.parse_args()
        key = data['key']
        value = data['value']

        current_user = UserModel.find_by_username(get_jwt_identity())

        if KeyValueModel.exists(current_user.id, key):
            KeyValueModel.update(current_user.id, key, value)
            return {'message': 'Successfully updated item'}
        else:
            newItem = KeyValueModel(
                key = key,
                value = value,
                user_id = current_user.id
            )

            try:
                newItem.add()
                return {'message': 'Successfully created item'}
            except:
                return {'message': 'Unable to create item'}, 500

class GetItems(Resource):
    @jwt_required
    def get(self):        
        current_user = UserModel.find_by_username(get_jwt_identity())

        return KeyValueModel.getAllForUser(current_user.id)

