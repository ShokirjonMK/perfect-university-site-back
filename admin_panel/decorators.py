from django.contrib.auth.decorators import user_passes_test
from rolepermissions.checkers import has_role


def only_admin(view_func=None, login_url="index-admin", message="Permission denied"):
    actual_decorator = user_passes_test(
        lambda u: has_role(u, ["admin"]) and u.is_active, login_url=login_url, redirect_field_name=""
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator
