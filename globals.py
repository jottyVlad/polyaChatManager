class Globals:
    db_engine = None

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Globals, cls).__new__(cls)
        return cls.instance # noqa
