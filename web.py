#coding:utf-8

import bottle
from Corellia.RedisQueue import TaskQueue, ResultAlreadyExpired, ResultNotReady
import yajl as json
from eurasia.web import wsgiserver, mainloop

from sys import argv
addr = argv[1]
if ":" in addr:
    host, port = addr.split(":")
    port = int(port)
else:
    host = addr
    port = 6379
port = int(port)

app = bottle.Bottle()

tq = TaskQueue(host, port, pickler=json)

@app.get("/")
def hello():
    return u"词句已成血肉"

@app.post("/<path:path>")
def push_task(path):
    try:
        queue, method = path.split("/")
    except:
        return None
    args = bottle.request.body.read()
    key = tq.call(queue, method, [args], async=True)
    bottle.response.set_header("key", key)

@app.get("/<path:path>")
def get_result(path):
    try:
        queue, _, key = path.split("/")
    except:
        return None
    try:
        result = tq.fetch_async_result(key)
        result = "ResultNotReady" if isinstance(result, ResultNotReady) else result
    except ResultAlreadyExpired:
        result = "ResultAlreadyExpired"
    return result

if __name__ == '__main__':
    # bottle.run(app, server='tornado', host='0.0.0.0')
    httpd = wsgiserver(':8080', app)
    httpd.start()
    mainloop()


