class TkinterVars:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TkinterVars, cls).__new__(cls, *args, **kwargs)
            cls._instance.vars = {}
        return cls._instance

    def set_var(self, name, var):
        self.vars[name] = var

    def get_var(self, name):
        return self.vars.get(name)