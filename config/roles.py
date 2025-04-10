from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        "manage": True,
    }


class Staff(AbstractUserRole):
    available_permissions = {
        "edit": True,
    }


class RegularUser(AbstractUserRole):
    available_permissions = {
        "view": True,
    }
