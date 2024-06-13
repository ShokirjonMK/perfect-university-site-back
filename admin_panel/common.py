from api import translate


# Auto generate model
def generate_field(field):
    try:
        result = translate.translate_to_latin(field)
        return result
    except Exception:
        pass


# Simple boolean checke for HTML checker
def boolen_checker(value):
    if value == "on":
        return True
    return False
