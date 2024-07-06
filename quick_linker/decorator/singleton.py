def Singleton(cls):
    _instance = {}
    def _singleton(*args, **kwargs):
        if cls not in _instance:
            try:
                _instance[cls] = cls(*args, **kwargs)
            except TypeError as te:
                print(f"TypeError: {te}")
                print(f"arguments required: {cls.__init__.__code__.co_varnames}")
                print(f"arguments provided: {args}")
        return _instance[cls]
    return _singleton
