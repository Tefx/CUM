from exports import export
import ujson as json

cdef class Worker(object):

    cdef dict mods

    def __cinit__(self, mod_path):
        self.mods = export(mod_path)

    cpdef eval(self, env):
        cdef dict res = {}
        env = json.loads(env)
        for k in env.iterkeys():
            if k[0] == "_":
                res[k] = self.cal(k, env)
        return res

    cpdef cal(self, name, env):
        var = env[name]
        if not isinstance(var, list):
            return var
        if var[0] == "!":
            mod = self.mods[var[1]]
            need_copy = False
            var = var[2:]
            len_var = len(var)
            marks = [0]*len_var
            for j in xrange(len_var):
                x = var[j]
                if isinstance(x, basestring):
                    if x[0] == "#":
                        x = x[1:]
                        marks[j] = -1
                        size = len(self.cal(x, env))
                        need_copy = True
                        var[j] = x
                    else:
                        self.cal(x, env)
                        marks[j] = 1
            if not need_copy:
                args = [env[var[i]] if marks[i] else var[i] for i in xrange(len_var)]
                env[name] = mod(*args)
            else:
                l = [0] * size
                l0 = [0] * len_var
                for i in xrange(size):
                    for j in xrange(len_var):
                        if marks[j] < 0:
                            l0[j] = env[var[j]][i]
                        elif marks[j] > 0:
                            l0[j] = env[var[j]]
                        else:
                            l0[j] = var[j]
                    l[i] = mod(*l0)
                env[name] = l
            return env[name]
        else:
            need_copy = False
            len_var = len(var)
            marks = [0]*len_var
            for j in xrange(len_var):
                x = var[j]
                if isinstance(x, basestring):
                    if x[0] == "#":
                        x = x[1:]
                        marks[j] = -1
                        size = len(self.cal(x, env))
                        need_copy = True
                        var[j] = x
                    else:
                        self.cal(x, env)
                        marks[j] = 1
            if not need_copy:
                env[name] = [env[var[i]] if marks[i] else var[i] for i in xrange(len_var)] 
            else:
                ls = [[0]*len_var for _ in xrange(size)]
                for i in xrange(size):
                    for j in xrange(len_var):
                        if marks[j] < 0:
                            ls[i][j] = env[var[j]][i]
                        elif marks[j] > 0:
                            ls[i][j] = env[var[j]]
                        else:
                            ls[i][j] = var[j]
                env[name] = ls
            return env[name]