from aiohttp import web


def msg_response(code=400, **msg):
    response = web.json_response(msg, status=code)
    return response
