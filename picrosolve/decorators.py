import functools

def memoize(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = "".join([str(arg) for arg in args]) + "".join([str(item) for item in sorted(kwargs.items(), key=lambda x: x[0])])
        if key not in cache:
            # print("key '{}' is not in cache yet".format(key))
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer
