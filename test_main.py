from main import User
from tinydb import TinyDB, table
from tinydb.storages import MemoryStorage
import pytest


@pytest.fixture
def setup_db():
    User.DB = TinyDB(storage=MemoryStorage)


@pytest.fixture
def user(setup_db):
    u = User(first_name="Aboubacar",
             last_name="Soumah",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    u.save()
    return u


def test_first_name(user):
    assert user.first_name == "Aboubacar"


def test_last_name(user):
    assert user.last_name == "Soumah"


def test_address(user):
    assert user.address == "1 rue du chemin, 75000 Paris"


def test_phone_number(user):
    assert user.phone_number == "0123456789"


def test_full_name(user):
    assert user.full_name == "Aboubacar Soumah"


def test_exists(user):
    assert user.exists() is True


def test_not_exists(setup_db):
    u = User(first_name="Aboubacar",
             last_name="Soumah",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.exists() is False


def test_db_instance(user):
    assert isinstance(user.db_instance, table.Document)
    assert user.db_instance["first_name"] == "Aboubacar"
    assert user.db_instance["last_name"] == "Soumah"
    assert user.db_instance["address"] == "1 rue du chemin, 75000 Paris"
    assert user.db_instance["phone_number"] == "0123456789"


def test_not_db_instance(setup_db):
    u = User(first_name="Aboubacar",
             last_name="Soumah",
             address="1 rue du chemin, 75000 Paris",
             phone_number="0123456789")
    assert u.db_instance is None


def test__check_number_with_user_good(setup_db):
    u = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    u.save(valid_data=True)
    assert u.exists()


def test__check_number_with_user_bad(setup_db):
    u = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="abc")
    with pytest.raises(ValueError) as err:
        u._check_number()
    assert "n'est pas valide" in str(err.value)


def test__check_names_empty(setup_db):
    u = User(first_name="", last_name="", address="05 rue belvedere", phone_number="0123456789")
    with pytest.raises(ValueError) as err:
        u._check_names()
    assert "Les champs nom et prénom ne doivent pas être vides" in str(err.value)


def test__check_names_invalid_characters(setup_db):
    u = User(first_name="Aboubacar*$", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    with pytest.raises(ValueError) as err:
        u._check_names()
    assert "est invalide" in str(err.value)


def test__check_names_with_good_user(setup_db):
    u = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    u.save(valid_data=True)
    assert u.exists() is True


def test_delete(setup_db):
    u = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    u.save()
    first = u.delete()
    second = u.delete()
    assert isinstance(first, list)
    assert isinstance(second, list)
    assert len(first) > 0
    assert len(second) == 0


def test_save(setup_db):
    u = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    u_duplicate = User(first_name="Aboubacar", last_name="Soumah", address="05 rue belvedere", phone_number="0123456789")
    first = u.save()
    second = u_duplicate.save()
    assert isinstance(first, int)
    assert isinstance(second, int)
    assert first > 0
    assert second == -1
