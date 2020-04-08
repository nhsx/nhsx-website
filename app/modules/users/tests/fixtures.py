# 3rd party
import json
from typing import List
import pytest

from modules.users.models import User

pytestmark = pytest.mark.django_db

def _create_user(first_name: str, last_name: str, email: str) -> User:
    """Abstracting this allows us to test more scenarios than just passing the
    fixture around.

    Args:
        first_name (str): The user's first name
        last_name (str): The user's last name

    Returns:
        SectionPage: User
    """
    user = User()
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()
    return user

@pytest.fixture(scope="function")
def user() -> User:
    p = _create_user('Foo', 'Bar', 'foo@example.com')
    return p

@pytest.fixture(scope="function")
def users() -> List[User]:
    """Fixture providing 10 BlogPost objects attached to blog_post_index_page
    """
    rv = []
    for _ in range(0, 10):
        p = _create_user('User', f'{_}', f'user{_}@example.com')
        rv.append(p)
    return rv
