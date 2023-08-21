from aiohttp import web
import json

async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


async def users(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    users = [{"id": 1, "name": "John"}, {"id": 1, "name": "Ajay"}]
    return web.Response(text=json.dumps(users))

app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/users', users),
                web.get('/{name}', handle),
                ])

if __name__ == '__main__':
    web.run_app(app)


"""
http://localhost:8080/
http://localhost:8080/aafak
http://localhost:8080/users
"""