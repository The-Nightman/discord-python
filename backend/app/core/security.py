import bcrypt


def get_password_hash(password: str) -> str:
    """
    Hashes a password using bcrypt.

    Remarks:
        passlib has not been maintained since 2020 and so despite having a module used
        in conjunction with bcrypt and its algorithms, it is not recommended to use it.

    Args:
        password (str): The plain text password to hash.

    Returns:
        str: The hashed password.
    """
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    )
