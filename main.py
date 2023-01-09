import asyncio, os
from aiohttp import web

loop=asyncio.get_event_loop()
routes = web.RouteTableDef()

with open("index.html") as f:
	index_contents=f.read()

@routes.get("/")
async def index(request):
	return web.Response(body=index_contents, content_type='text/html')

@routes.post("/file_sent")
async def store(request):
	reader = await request.multipart()

	field = await reader.next()
	assert field.name == 'upload'
	filename = field.filename
	# You cannot rely on Content-Length if transfer is chunked.
	size = 0
	with open(os.path.join('uploads/', filename), 'wb') as f:
		while True:
			chunk = await field.read_chunk()  # 8192 bytes by default.
			if not chunk:
				break
			size += len(chunk)
			f.write(chunk)

	return web.Response(body='Thank you for your submission', content_type='text/html')

http_server=web.Application()
http_server.add_routes(routes)

loop.create_task(web._run_app(http_server,host='0.0.0.0',port=8000))
loop.run_forever()
