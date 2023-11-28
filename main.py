from tinydb import TinyDB, Query, table
from pathlib import Path
import string


class User:

    DB = TinyDB(Path(__file__).resolve().parent / "data.json", indent=4)

    def __init__(self, first_name: str, last_name: str, phone_number: str = "", address: str = ""):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address

    def __str__(self):
        return f"Nom de l'utilisateur: {self.full_name}\nTelephone: {self.phone_number}\nAdrresse: {self.address}"

    def __repr__(self):
        return f"User({self.first_name},{self.last_name})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def _checks(self):
        self._check_number()
        self._check_names()

    def _check_number(self):
        if self.phone_number:
            self.phone_number = "".join(
                number for number in self.phone_number if number not in ["(", ")", "+", " ", "-"])
            if not self.phone_number.isdigit() or len(self.phone_number) < 8:
                raise ValueError(
                    f"Le numero de télephone {self.phone_number} n'est pas valide")

    def _check_names(self):
        if not (self.first_name and self.last_name):
            raise ValueError(
                "Les champs nom et prénom ne doivent pas être vides")
        special_caracteres = string.punctuation + string.digits
        if any(letter in special_caracteres for letter in self.first_name + self.last_name):
            raise ValueError(f"le nom {self.full_name} est invalide")

    @property
    def db_instance(self) -> table.Document:
        u = Query()
        return User.DB.get((u.first_name == self.first_name) & (u.last_name == self.last_name))

    def exists(self):
        return bool(self.db_instance)

    def delete(self) -> list[int]:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])
        return []

    def save(self, valid_data=False):
        if valid_data:
            self._checks()
        return -1 if self.exists() else User.DB.insert(self.__dict__)


def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__":
   pass
