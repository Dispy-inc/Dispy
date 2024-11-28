class dict_to_obj(dict):
    def __getattr__(self, attr):
        value = self.get(attr)
        if isinstance(value, dict):
            return dict_to_obj(value)
        return value
    
def format_list(elements):
    if not elements:
        return ""
    elif len(elements) == 1:
        return elements[0]
    elif len(elements) == 2:
        return " and ".join(elements)
    else:
        return ", ".join(elements[:-1]) + " and " + elements[-1]