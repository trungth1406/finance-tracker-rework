from abc import ABC
import uuid


class IncomeSource(ABC):
    def __init__(self, name, amount):
        self.id = uuid.uuid4()
        self.name = name
        self.amount = amount

    @property
    def get_id(self):
        return self.id

    @property
    def get_name(self):
        return self.name

    @property
    def get_amount(self):
        return self.amount

    def create_account(self, name, with_amount):
        account = Account(name, self)
        account.withdraw_from_resource(with_amount)
        return account

    def add(self, amount):
        self.amount += amount
        return self

    def take(self, amount):
        self.amount -= amount
        return self


class Account:

    def __init__(self, name, from_resource):
        self.uuid = uuid.uuid4()
        self.name = name
        self.amount = 0
        self.from_resource = from_resource

    @classmethod
    def init_from_resource(cls, name, resource):
        return cls(name, resource)

    @property
    def get_id(self):
        return self.uuid

    @property
    def get_name(self):
        return self.name

    @property
    def get_remain_in_account(self):
        return self.amount

    def withdraw_from_resource(self, amount):
        if self.from_resource.amount < amount:
            raise ValueError("The Account to transfer money does not have enough money")
        self.from_resource.take(amount)
        self.amount += amount

    def withdraw(self, amount):
        if amount > self.amount:
            raise ValueError("The withdrawal money is greater than current money in the account")
        self.amount -= amount
        return self
