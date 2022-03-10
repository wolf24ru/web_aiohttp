import views

from aiohttp import web
from new_app import app
from models import init_orm


if __name__ == '__main__':
    app.cleanup_ctx.append(init_orm)
    web.run_app(app, host='0.0.0.0', port=8080)
