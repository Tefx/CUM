# from gevent import monkey; monkey.patch_all()
from Corellia.RedisQueue import Client
# import time
import yajl as json

c = Client("192.168.70.150", 6379, "CUM", pickler=json)

# g = {
#     "a" : 1,
#     "b" : 2,
#     "c" : 3,
#     "d" : 4,
#     "e" : ["!", "test.m1", "a", "b"],
#     "f" : ["!", "test.m2", "e"],
#     "g" : ["!", "test.m3", "b", "c", "f"],
#     "h" : [1, 3, 5, 7],
#     "i" : [1, 2, 3, 4],
#     "_u": ["!", "test.m4", "h", "#i", "g"]
#     }


# v = c.eval(g)
# print v
# # print c.fetch_result(v)
# time.sleep(2)
# print c.fetch_result(v)

s = {
  "P"                   : [0.42, 0.43] * 10,
  "V"                   : [25, 25] * 10,
  "T"                   : [1, 1.3] * 10,
  "M"                   : [0.5036, 0.478] * 10,
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

# import requests
# import timeit

# print json.loads(s)

# def test_http():
#     baseurl = "http://localhost:8080/"
#     r = requests.post(baseurl+"CUM/eval", data=s, headers={'content-type': 'application/json'})
#     result_url = baseurl + "CUM/eval/" + r.headers["key"]
#     print result_url
#     while True:
#         r = requests.get(result_url)
#         print r
#         if r.json:
#             print r.json
#             break
#         time.sleep(0.2)

# test_http()
import gevent

def sync_call():
  let = []
  for i in xrange(100):
    let.append(gevent.spawn(lambda s:c.eval(s), s))
  gevent.joinall(let)

# t = timeit.Timer("sync_call()", "from __main__ import sync_call")
# print t.repeat(1, 1)

sync_call()

# import profile
# profile.run("c.eval(s)", "prof.txt")
# import pstats
# p = pstats.Stats("prof.txt")
# p.sort_stats("cumulative").print_stats()

# print c.eval(s)
