from passlib.apps import custom_app_context as pwd_context

from new_app import db, app
from config import POSTGRE_URI


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # advertisements = db.relationship('Advertisement', backref='users', lazy=True)

    __idx1 = db.Index('app_user_username', 'username', unique=True)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def to_dict(self):
        return {
            'user_id': self.id,
            'user_name': self.username,
            # TODO создать функцию для получения объявлений конкретного пользователя
            # 'advertisements': self.advertisements
        }



class Advertisement(db.Model):
    __tablename__ = 'advertisements'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    create_date = db.Column(db.DateTime(), nullable=False)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    __idx1 = db.Index('advertisement_title', 'title', unique=True)

    @property
    def __date_serialize(self):
        return f'{self.create_date.strftime("%d.%m.%Y %H:%M")}'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'create_date': self.__date_serialize,
            'owner': self.owner
        }


async def init_orm(app):
    # приложение стартовало и работает
    await db.set_bind(POSTGRE_URI)
    await db.gino.create_all()
    yield
    await db.pop_bind().close()
