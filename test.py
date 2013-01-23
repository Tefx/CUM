from gevent import monkey; monkey.patch_all()
from Corellia.client import Client
import ujson
import requests
import gevent
import timeit
from gevent.pool import Pool
pool = Pool(1000)
import threading
import time
s = {
  "P"                   : [0.42, 0.43],
  "V"                   : [25, 25],
  "T"                   : [1, 1.3],
  "M"                   : [0.5036, 0.478],
  "W"                   : ["!", "mode0", "#P", "#V", "#T", "#M"],
  "MPE"                 : 0.0002,
  "K"                   : 1.732,
  "Urel1"               : ["!", "mode1", "MPE", "K", "#M"],
  "Tm"                  : 19.4,
  "K1"                  : 3.464,
  "Ni"                  : [19.6, 19.5, 18.3, 19.6, 20.4, 18.6, 20.2, 18.9, 19.7, 20, 18.8],
  "Urel2"               : ["!", "mode2", "Tm", "K1", "Ni"],
  "MPE2"                : 0.03,
  "Vm"                  : 25,
  "K2"                  : 1.732,
  "Urel3"               : ["!", "mode1", "MPE2", "K2", "Vm"],
  "Temp"                : 3,
  "Times"               : 6,
  "K3"                  : 1.732,
  "Coefficient"         : 0.00021,
  "Pm"                  : [10, 100, 5, 100, 5, 25],
  "Urel4"               : ["!", "mode3", "Temp", "Times", "K3", "Coefficient"],
  "K4"                  : 1.732,
  "liquorConcentration" : 1000,
  "maxConcentration"    : 1,
  "MPE3"                : 3,
  "Urel5"               : ["!", "mode1", "MPE3", "K4", "liquorConcentration"],
  "K5"                  : 1.732,
  "perError"            : [0.02, 0.1, 0.1, 0.015, 0.025, 0.03 ],
  "perVolumn"           : [10, 100, 100, 5, 5, 25],
  "Urel6"               : ["!", "mode4", "K5", "perError", "perVolumn" ],
  "Times2"              : 3,
  "Pi"                  : [0, 0.2, 0.4, 0.6, 0.8, 1],
  "Ai"                  : [0.0017, 0.0185, 0.0345, 0.0536, 0.0696, 0.0859, 0.0006, 0.0189, 0.0349, 0.0517, 0.0698, 0.0876, 0, 0.0181, 0.0349, 0.0528, 0.0692, 0.0842, 0.003, 0.0165, 0.0349, 0.0537, 0.0701, 0.0868],
  "Urel7"               : ["!", "mode5", "Times2", "Pi", "Ai", "#P" ],
  "K6"                  : 2,
  "Urels"               : ["#Urel1", "Urel2", "Urel3", "Urel4", "Urel5", "Urel6", "#Urel7"],
  "_U"                  : ["!", "modef", "#Urels", "#W", "K6" ]
}

import urllib2
import urllib

s = ujson.dumps(s)

def test_http(i):
    baseurl = "http://localhost:8080/"
    r = urllib2.Request(baseurl+"CUM/eval", s, headers={"Content-Type":"application/json"})
    try:
      key = urllib2.urlopen(r).headers["key"]
      result_url = baseurl + "CUM/" + key
      # print result_url
      while True:
          result = urllib2.urlopen(result_url).read()
          if result == "ResultNotReadyOrExpired":
              time.sleep(0.01)
          else:
              # print result
              break
    except:
      pass

# test_http(0)

def test_http_n(n):
  ts = [threading.Thread(target=test_http, args=(i,)) for i in xrange(n)]
  # for t in ts:
  #   t.start()
  # for t in ts:
  #   t.join()
  pool.map(test_http, xrange(n))

c = Client("localhost", "CUM", pickler=ujson, serialize=True, interval=0.1)

def test_pt(n):
  for i in xrange(n):
    c.put_task("eval", (s,), str(i))
  c.finish()

def test_gr(n):
  pool.map(lambda i:c.get_result(str(i)), xrange(n))

def sync_call(n):
  # ts = [threading.Thread(target=c.eval, args=(s,)) for _ in xrange(n)]
  # for t in ts:
  #   t.start()
  # for t in ts:
  #   t.join()
  pool.map(lambda _:c.eval(s), xrange(n))


# print c.eval(s)

t = timeit.Timer("test_http_n(1000)", "from __main__ import test_http_n")
print t.repeat(1, 1)

# t = timeit.Timer("test_pt(1000)", "from __main__ import test_pt")
# print t.repeat(1, 1)

# t = timeit.Timer("test_gr(1)", "from __main__ import test_gr")
# print t.repeat(1, 1)

# t = timeit.Timer("sync_call(1000)", "from __main__ import sync_call")
# print t.repeat(10, 1)

# import cProfile as profile
# profile.run("test_http_n(100)", "prof.txt")
# import pstats
# p = pstats.Stats("prof.txt")
# p.sort_stats("cumulative").print_stats() 



