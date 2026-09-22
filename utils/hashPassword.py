from django.contrib.auth.hashers import make_password


def hash_password(password: str) -> str:
    return make_password(password)
