from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, asynchronous
from Corellia.taskqueue import ResultNotReadyOrExpired
from multiprocessing.pool import ThreadPool
 
_workers = ThreadPool(200)
 
# def run_background(func, callback, args=(), kwds={}):
#     def _callback(result):
#         IOLoop.instance().add_callback(lambda: callback(result))
#     _workers.apply_async(func, args, kwds, _callback)

class CUMHandler(RequestHandler):
    def initialize(self, client):
        self.client = client

    @asynchronous
    def post(self, method):
        key = self.client.put_task(method, (self.request.body,))
        self.set_header("key", key)
        self.finish()

    def get_result(self, key):
        try:
            result = self.client.get_result(key)
        except ResultNotReadyOrExpired:
            result = "ResultNotReadyOrExpired"
        # return result
        IOLoop.instance().add_callback(lambda: self.on_complete(result))

    def on_complete(self, result):
        self.write(result)
        self.finish()

    @asynchronous
    def get(self, key):
        _workers.apply_async(self.get_result, (key,))

if __name__ == '__main__':
    from sys import argv
    import ujson as json
    from Corellia.client import Client

    if len(argv) < 2:
        addr = "localhost"
    else:
        addr = argv[1]

    client = Client(addr, "CUM", pickler=json, serialize=True, interval=0.1)
    Application([
        ("/CUM/(.*)", CUMHandler, dict(client=client)),
    ]).listen(8080)
    IOLoop.instance().start()