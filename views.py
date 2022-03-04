from datetime import datetime
# from flask import jsonify, g, request
# from flask.views import MethodView
# from flask_httpauth import HTTPBasicAuth
from passlib.apps import custom_app_context as pwd_context


from schema import NEW_USER, NEW_THING




from passlib.apps import custom_app_context as pwd_context
from models import User, Advertisement
from validator import UserModelValidator
from error import msg_response
from aiohttp import web
from new_app import db, app

import pydantic
import json


async def check_health(request: web.Request):
    return web.json_response({'STATUS': 'OK'})


class UserView(web.View):
    def hash_password(self, password):
        return pwd_context.encrypt(password)

    async def get(self):
        user_id = int(self.request.match_info['user_id'])
        user_data = await User.get(user_id)
        if user_data:
            return web.json_response(user_data.to_dict())
        else:
            return msg_response(error='user not found')

    async def post(self):
        user_data_request = await self.request.json()
        try:
            user_data = UserModelValidator(**user_data_request).dict()
        except pydantic.error_wrappers.ValidationError as er:
            return msg_response(json.loads(er.json()))
        user_name = user_data['user_name']
        user_passwd = user_data['password']
        new_user = await User.create(
            username=user_name,
            password_hash=self.hash_password(user_passwd))
        return web.json_response(new_user.to_dict())

class AdvertisementView(web.View):
    async def verify_password(self, user_name, password):
        user = await User.get(user_name)
        if not user or not user.verify_password(password):
            return False
        return True

    async def get(self):
        adv_id = int(self.request.match_info['adv_id'])
        if adv_id:
            adv_data = await Advertisement.get(adv_id)
            if adv_data:
                return web.json_response(adv_data.to_dict())
            else:
                return msg_response(msg='user not exist')
        else:
            adv_all = await Advertisement.query.gino.all()
            response = web.json_response(
                {'json_list':[adv_.to_dict() for adv_ in adv_all]}
            )
            return response
app.add_routes([web.get('/health', check_health)])

app.add_routes([web.get('/get_user/{user_id:\d+}', UserView)])
app.add_routes([web.post('/new_user', UserView)])

app.add_routes([web.get('/adv/{adv_id:\d+}', UserView)])
app.add_routes([web.get('/adv', UserView)])

# class UserView(MethodView):

#     @auth.verify_password
#     def verify_password(self, user_name, password):
#         user = User.query.filter_by(username=user_name).first()
#         if not user or not user.verify_password(password):
#             return False
#         g.user = user
#         return True
#
#     def get(self, user_id):
#         if user_id is None:
#             return msg_response(msg='id is none')
#         user = User.query.filter_by(id=user_id).first()
#         if user is None:
#             return msg_response(msg=f'user {user_id} not exist')
#         return jsonify(user.to_dict())
#
#     def post(self,):
#         try:
#             jsonschema.validate(request.json, NEW_USER)
#             user_name = request.json['user_name']
#             password = request.json['password']
#             self.hash_password(password)
#             if user_name is None or password is None:
#                 return msg_response(msg='user name or password is none')
#             user = User.query.filter_by(username=user_name).first()
#             if user is not None:
#                 return msg_response(msg='user exist')
#             user = User(username=user_name)
#             user.hash_password(password)
#             db.session.add(user)
#             db.session.commit()
#             response = jsonify(user.to_dict())
#             response.status_code = 201
#             return response
#         except jsonschema.ValidationError as er:
#             return msg_response(error=er.message)

# class AdvertisementView(MethodView):
#     def get(self, **adv):
#         if adv:
#             adv_first = Advertisement.query.filter_by(id=adv['adv_id']).first()
#             if adv_first is not None:
#                 response = jsonify(adv_first.to_dict())
#             else:
#                 return msg_response(msg='user not exist')
#         else:
#             adv_all = Advertisement.query.all()
#             response = jsonify(json_list=[adv_.to_dict() for adv_ in adv_all])
#         return response
#
#     def post(self):
#         try:
#             jsonschema.validate(request.json, NEW_THING)
#             user_name = request.json['user_name']
#             password = request.json['password']
#             if self.verify_password(user_name, password):
#                 title = request.json['title']
#                 description = request.json['description']
#                 date = datetime.now()
#                 user = User.query.filter_by(username=user_name).first()
#                 adv = Advertisement(title=title,
#                                     description=description,
#                                     create_date=date,
#                                     owner=user.id)
#                 db.session.add(adv)
#                 db.session.commit()
#                 return msg_response(201, data='Advertisement successful create',
#                                     title=title,
#                                     description=description,
#                                     create_date=date,
#                                     owner=user.username)
#             else:
#                 return msg_response(401, error='User not verification')
#         except jsonschema.ValidationError as er:
#             return msg_response(error=er.message)
#
#     def __check_owner(self, user_name,  adv_id):
#         user = User.query.filter_by(username=user_name).first().advertisements
#         for adv in user:
#             if adv.id == int(adv_id):
#                 return True
#         return False
#
#     def delete(self, adv_id):
#         try:
#             jsonschema.validate(request.json, NEW_USER)
#             user_name = request.json['user_name']
#             password = request.json['password']
#             if self.verify_password(user_name, password):
#                 if self.__check_owner(user_name, adv_id):
#                     adv = Advertisement.query.filter_by(id=adv_id).first()
#                     db.session.delete(adv)
#                     db.session.commit()
#                     response = jsonify(data=f'Advertisement {adv_id} delete')
#                     return response
#                 else:
#                     response = jsonify(data=f'you not owner advertisement {adv_id}. Error delete')
#                     response.status_code = 400
#                     return response
#             else:
#                 return msg_response(401, error='User not verification')
#         except jsonschema.ValidationError as er:
#             return msg_response(error=er.message)
#
#     def patch(self, adv_id):
#         try:
#             jsonschema.validate(request.json, NEW_USER)
#             json_request = request.json
#             user_name = json_request.pop('user_name')
#             password = json_request.pop('password')
#             if self.verify_password(user_name, password):
#                 if self.__check_owner(user_name, adv_id):
#                     adv = Advertisement.query.filter_by(id=adv_id).first()
#                     for update_key, update_value in json_request.items():
#                         match update_key:
#                             case 'title':
#                                 adv.title = update_value
#                             case 'description':
#                                 adv.title = update_value
#                     db.session.commit()
#                     return msg_response(200, data=f'Advertisement {adv_id} update')
#                 else:
#                     return msg_response(data=f'you not owner advertisement {adv_id}. Error delete')
#             else:
#                 return msg_response(401, error='User not verification')
#         except jsonschema.ValidationError as er:
#             return msg_response(error=er.message)
#
#
# app.add_url_rule('/new_user/', view_func=UserView.as_view('new_user'), methods=['POST'])
# app.add_url_rule('/get_use/<user_id>', view_func=UserView.as_view('get_user'), methods=['GET'])
#
# app.add_url_rule('/adv/<adv_id>', view_func=AdvertisementView.as_view('get_adv_id'), methods=['GET'])
# app.add_url_rule('/adv/', view_func=AdvertisementView.as_view('get_adv'), methods=['GET'])

# app.add_url_rule('/adv_new/', view_func=AdvertisementView.as_view('adv_new'), methods=['POST'])
# app.add_url_rule('/adv_del/<adv_id>', view_func=AdvertisementView.as_view('del_adv'), methods=['DELETE'])
# app.add_url_rule('/adv_patch/<adv_id>', view_func=AdvertisementView.as_view('patch_adv'), methods=['PATCH'])
