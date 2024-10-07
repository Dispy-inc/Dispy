class dict_to_obj(dict):
    def __getattr__(self, attr):
        value = self.get(attr)
        if isinstance(value, dict):
            return dict_to_obj(value)
        return value