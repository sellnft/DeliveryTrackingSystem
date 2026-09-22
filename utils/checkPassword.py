from django.contrib.auth.hashers import check_password


def verify_password(password: str, password_hash: str) -> bool:
    return check_password(password, password_hash)
