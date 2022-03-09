import asyncpg
import pydantic
import json

from datetime import datetime
from passlib.apps import custom_app_context as pwd_context

from models import User, Advertisement
from validator import UserModelValidator, AdvertisementModelValidator
from error import msg_response
from aiohttp import web
from new_app import app


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
    async def verify_password(self, user_name: str, password: str):
        user = await User.query.where(
            User.username == user_name).gino.first()
        if not user or not user.verify_password(password):
            return False
        return True

    async def check_owner(self, user_name: str, adv_id: int):
        adv = await Advertisement.get(adv_id)
        user = await User.query.where(
            User.username == user_name).gino.first()
        if adv.owner == user.id:
            return True
        return False

    async def get(self):
        try:
            adv_id = int(self.request.match_info['adv_id'])
        except KeyError as er:
            adv_id = None
        if adv_id:
            adv_data = await Advertisement.get(adv_id)
            if adv_data:
                return web.json_response(adv_data.to_dict())
            else:
                return msg_response(msg='user not exist')
        else:
            adv_all = await Advertisement.query.gino.all()
            response = web.json_response(
                {'json_list': [adv_.to_dict() for adv_ in adv_all]}
            )
            return response

    async def post(self):
        adv_data_request = await self.request.json()
        try:
            adv_data = AdvertisementModelValidator(**adv_data_request).dict()
        except pydantic.error_wrappers.ValidationError as er:
            return msg_response(json.loads(er.json()))
        user_name = adv_data['user_name']
        user_passwd = adv_data['password']
        if await self.verify_password(user_name, user_passwd):
            title = adv_data['title']
            description = adv_data['description']
            date = datetime.now()
            user = await User.query.where(
                User.username == user_name).gino.first()
            try:
                new_adv = await Advertisement.create(title=title,
                                                     description=description,
                                                     create_date=date,
                                                     owner=user.id)
                return msg_response(201, **new_adv.to_dict())
            except asyncpg.exceptions.UniqueViolationError as er:
                return msg_response(401, error='error create object of advertisement. Check your data and try again')
        else:
            return msg_response(401, error='User not verification')

    async def delete(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv_data_request = await self.request.json()
        try:
            adv_data = UserModelValidator(**adv_data_request).dict()
        except pydantic.error_wrappers.ValidationError as er:
            return msg_response(error=er.json())
        user_name = adv_data['user_name']
        user_passwd = adv_data['password']
        if await self.verify_password(user_name, user_passwd):
            if await self.check_owner(user_name, adv_id):
                delete = await Advertisement.get(adv_id)
                await delete.delete()
                return msg_response(200, error=f'Advertisement {adv_id} delete')
            else:
                return msg_response(error=f'you not owner advertisement {adv_id}. Error delete')
        else:
            return msg_response(401, error='User not verification')

    async def patch(self):
        adv_id = int(self.request.match_info['adv_id'])
        adv_data_request = await self.request.json()
        try:
            adv_data = AdvertisementModelValidator(**adv_data_request).dict()
        except pydantic.error_wrappers.ValidationError as er:
            return msg_response(json.loads(er.json()))
        user_name = adv_data['user_name']
        user_passwd = adv_data['password']
        if await self.verify_password(user_name, user_passwd):
            if await self.check_owner(user_name, adv_id):
                adv = await Advertisement.get(adv_id)
                for update_key, update_value in adv_data_request.items():
                    match update_key:
                        case 'title':
                            await adv.update(title=update_value).apply()
                        case 'description':
                            await adv.update(update_value).apply()
                return msg_response(200, data=f'Advertisement {adv_id} update')
            else:
                return msg_response(error=f'you not owner advertisement {adv_id}. Error delete')
        else:
            return msg_response(401, error='User not verification')


app.add_routes([web.get('/health', check_health)])

app.add_routes([web.get('/get_user/{user_id:\d+}', UserView)])
app.add_routes([web.post('/new_user', UserView)])

app.add_routes([web.get('/adv/{adv_id:\d+}', AdvertisementView)])
app.add_routes([web.get('/adv', AdvertisementView)])
app.add_routes([web.post('/adv_new', AdvertisementView)])
app.add_routes([web.delete('/adv_del/{adv_id:\d+}',AdvertisementView)])
app.add_routes([web.patch('/adv_patch/{adv_id:\d+}',AdvertisementView)])
