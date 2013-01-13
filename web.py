import bottle
from Corellia.RedisQueue import Client, ResultAlreadyExpired, ResultNotReady
import yajl as json

@bottle.post("/<path:path>")
def push_task(path):
    try:
        queue, method = path.split("/")
    except:
        return None
    c = Client("localhost", 6379, queue, async=True, pickler=json)
    args = bottle.request.json
    args = [args] if not isinstance(args, list) else args
    key = getattr(c, method)(*args)
    bottle.response.set_header("key", key)

@bottle.get("/<path:path>")
def get_result(path):
    try:
        queue, _, key = path.split("/")
    except:
        return None
    c = Client("localhost", 6379, queue, async=True, pickler=json)
    try:
        result = c.fetch_result(key)
        result = "ResultNotReady" if isinstance(result, ResultNotReady) else result
    except ResultAlreadyExpired:
        result = "ResultAlreadyExpired"
    bottle.response.content_type = "application/json"
    return json.dumps(result)

if __name__ == '__main__':
    bottle.run(host='0.0.0.0')


