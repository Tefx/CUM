from exports import export
import json as json


class Worker(object):
    def __init__(self, mod_path):
        self.mods = export("CUM_Mod_Library")

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
    from sys import argv
    from Corellia.RedisQueue import Worker as CorellianWorker
    host, port, mod_path = argv[1:4]
    port = int(port)
    queue_name = "CUM"
    CorellianWorker(host, port, queue_name, json).run(Worker, mod_path)


