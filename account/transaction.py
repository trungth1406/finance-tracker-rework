from abc import ABC, abstractmethod
from datetime import date

from account.resource import Account, IncomeSource


class Transaction(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_date(self):
        pass

    @abstractmethod
    def get_transaction_amount(self):
        pass


class AccountTransaction(Transaction):

    def __init__(self, date_of_execution, from_acc):
        self.name = ""
        self.date = date_of_execution
        self.account = from_acc
        self.transaction_amount = 0

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date if self.date is not None else date.today()

    def get_transaction_amount(self):
        return self.transaction_amount

    def withdraw_from(self, from_source, amount):
        if type(from_source) is not IncomeSource:
            raise ValueError("Account to transfer from and to mus be of Source type")
        self.account.withdraw_from_resource(amount)
        self.transaction_amount = amount
        self.name = f"Withdraw from resource {from_source.get_name}"
        return self

    def withdraw(self, amount, reason):
        self.account.withdraw(amount)
        self.transaction_amount = amount
        self.name = f"Withdraw money for {reason} "
        return self
