

def get_class_name(obj_type):
    """gets the literal name from a class type"""
    return obj_type.__class__.strip("<class '", "'>")
