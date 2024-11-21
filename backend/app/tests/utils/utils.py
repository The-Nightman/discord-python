import random
import string
from faker import Faker


fake = Faker()


def random_lower_string(length: int) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_username() -> str:
    return fake.user_name()


def random_email() -> str:
    return fake.ascii_free_email()


def random_password() -> str:
    return fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
