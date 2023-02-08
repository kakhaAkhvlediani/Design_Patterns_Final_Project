import pytest

from app.core.users.interactor import User


@pytest.fixture
def user() -> User:
    username: str = "Lean"
    password: str = "password"

    return User(_user_id=0, _username=username, _password=password)


def test_user_id(user: User) -> None:
    assert user.get_user_id() == 0


def test_username(user: User) -> None:
    assert user.get_username() == "Lean"


def test_password(user: User) -> None:
    assert user.get_password() == "password"


def test_equals_method(user: User) -> None:
    username: str = "Lean"
    password: str = "password"

    assert User(_user_id=0, _username=username, _password=password) == user


def test_user_to_dict(user: User) -> None:
    assert user.to_dict() == {
        "user_id": user.get_user_id(),
        "username": user.get_username(),
        "password": user.get_password(),
    }


def test_user_id_neg(user: User) -> None:
    assert user.get_user_id() != -12


def test_username_neg(user: User) -> None:
    assert user.get_username() != "password"


def test_password_neg(user: User) -> None:
    assert user.get_password() != "Lean"


def test_equals_method_neg(user: User) -> None:
    username: str = "Lean"
    password: str = "password"

    assert User(_user_id=0, _username=password, _password=username) != user


def test_equals_method_different_id(user: User) -> None:  # NOT COMPARING WITH IDS
    username: str = "Lean"
    password: str = "password"

    assert User(_user_id=1, _username=username, _password=password) == user


def test_user_to_dict_neg_id(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id() + 2,
        "username": user.get_username(),
        "password": user.get_password(),
    }


def test_user_to_dict_neg_username(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
        "username": user.get_username() + "ra",
        "password": user.get_password(),
    }


def test_user_to_dict_neg_password(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
        "username": user.get_username(),
        "password": user.get_password() + "mehe",
    }


def test_user_to_dict_neg_no_username_field(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
        "password": user.get_password(),
    }


def test_user_to_dict_neg_no_password_field(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
        "username": user.get_username(),
    }


def test_user_to_dict_neg_no_username_and_password_fields(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
    }


def test_user_to_dict_neg_no_user_id_and_password_fields(user: User) -> None:
    assert user.to_dict() != {
        "username": user.get_username(),
    }


def test_user_to_dict_neg_no_id_and_username_fields(user: User) -> None:
    assert user.to_dict() != {
        "password": user.get_password(),
    }


def test_user_to_dict_neg_empty(user: User) -> None:
    assert user.to_dict() != {}


def test_user_to_dict_neg_extra_field(user: User) -> None:
    assert user.to_dict() != {
        "user_id": user.get_user_id(),
        "username": user.get_username(),
        "password": user.get_password(),
        "api_key": "admin_api_key",
    }


def test_user_equals_on_other_object(user: User) -> None:
    assert user != user.to_dict()
