from exports import export
import json as json


class Worker(object):
    def __init__(self):
        self.mods = export("mod_lib")

    def eval(self, env):
        # env = json.loads(env)
        res = {}
        for k in env.iterkeys():
            if k.startswith("_"):
                res[k] = self.cal(k, env)
        return res

    def cal(self, name, env):
        if not isinstance(name, unicode):
            return name
        if name[0] == "\\\"" and name[-1] == "\\\"":
            return name[1:-1]
        var = env.get(name, None)
        if not isinstance(var, list):
            return var
        if var[0] == "!":
            mod = self.mods[var[1]]
            args = [x for x in self.copy_args(var[2:], env)]
            env[name] = [mod(*arg) for arg in args]
            if len(env[name]) == 1:
                env[name] = env[name][0]
            return env[name]
        else:
            args = [x for x in self.copy_args(var, env)]
            args = args[0] if len(args) == 1 else args
            env[name] = args
            return args

    def copy_args(self, names, env):
        m = 1
        for name in names:
            if isinstance(name, unicode) and name.startswith("#"):
                m = max(m, len(self.cal(name[1:], env)))
            else:
                self.cal(name, env)
        for i in xrange(m):
            yield [self.nth(name, env, i) for name in names]

    def nth(self, name, env, n):
        if not isinstance(name, unicode):
            return self.cal(name, env)
        if name.startswith("#"):
            return self.cal(name[1:], env)[n]
        else:
            return self.cal(name, env)  


if __name__ == '__main__':
    # from Corellia.RedisQueue import Worker as CorellianWorker
    # host = "localhost"
    # port = 6379
    # queue_name = "CUM"
    # CorellianWorker(host, port, queue_name, json).run(Worker)

    s = {
      "P"                   : [0.42, 0.43] * 500,
      "V"                   : [25, 25] * 500,
      "T"                   : [1, 1.3] * 500,
      "M"                   : [0.5036, 0.478] * 500,
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

    import json

    s = json.dumps(s)
    s = json.loads(s)

    for _ in xrange(1):
      print Worker().eval(s)

    # import profile
    # profile.run("Worker().eval(s)", "prof.txt")
    # import pstats
    # p = pstats.Stats("prof.txt")
    # p.sort_stats("cumulative").print_stats()


