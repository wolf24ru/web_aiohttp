import asyncio
from gino import Gino
from aiohttp import web

app = web.Application()
db = Gino()
