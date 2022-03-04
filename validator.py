import pydantic


class UserModelValidator(pydantic.BaseModel):
    user_name: str
    password: str


class AdvertisementModelValidator(pydantic.BaseModel):
    user_name: str
    password: str
    title: str
