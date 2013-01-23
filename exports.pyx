import os,sys


cpdef export(str path):
    cdef dict exports = {}
    cdef int len_pre = len(path)
    cdef str basename
    cdef mod
    cdef str name
    cdef mods
    for root, _, files in os.walk(path):
        sys.path.insert(0, root)
        for f_name in files:
            if f_name[-3:] == ".py":
                basename = f_name[:-3]
                mod = __import__(basename)
                if basename != "defaults":
                    name = ".".join([root[len_pre:].replace(os.path.sep, "."), basename])
                    mods = {".".join([name.strip("."), k]):v for k,v in getattr(mod, "EXPORTS", {}).iteritems()}
                else:
                    mods = {k:v for k,v in getattr(mod, "EXPORTS", {}).iteritems()}
                exports.update(mods)
        del sys.path[0]
    return exports


