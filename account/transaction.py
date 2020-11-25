from abc import ABC, abstractmethod
from datetime import date

from account.resource import Account


class Transaction(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_date(self):
        pass


class AccountTransaction(Transaction):

    def __init__(self, name, date):
        self.name = name
        self.date = date

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date if self.date is None else date.today()

    def transfer(self, from_acc, to_acc, amount):
        if type(from_acc) and type(to_acc) is not Account:
            raise ValueError("Account to transfer from and to mus be of Account type")
        from_acc.withdraw_from(to_acc, amount)
