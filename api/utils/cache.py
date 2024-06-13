class CacheTypes:
    reset_password_verification = "reset_password_verification"

    @classmethod
    def get_verification_types(cls):
        type_list = [
            cls.reset_password_verification
        ]
        return type_list


def generate_cache_key(type_, *args):
    """
    Generate cache key for cache.set() and cache.get()
    args:
        - type:
        - email
        - session
    """
    return f"{type_}{''.join(args)}"


__all__ = ["CacheTypes", "generate_cache_key"]
