from gevent import monkey;monkey.patch_all()
from evaluation import Worker
from sys import argv
from Corellia.worker import WorkerPool
import ujson
addr, mod_path = argv[1:3]
queue_name = "CUM"
WorkerPool(addr, queue_name, pickler=ujson, serialize=True, interval=0.1, mass=False, num=5).run(Worker, mod_path)


