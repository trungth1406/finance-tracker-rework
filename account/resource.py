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

    def add(self, amount):
        self.amount += amount
        return self

    def take(self, amount):
        self.amount -= amount
        return self


class Account:

    def __init__(self, name, limit):
        self.uuid = uuid.uuid4()
        self.name = name
        self.amount = 0
        self.limit = limit

    @property
    def get_id(self):
        return self.uuid

    @property
    def get_name(self):
        return self.name

    @property
    def get_amount(self):
        return self.amount

    @property
    def get_limit(self):
        return self.limit

    def withdraw_from(self, account, amount):
        if account is not Account:
            raise ValueError("Need to pass in another Account")
        if account.get_amount < amount:
            raise ValueError("The Account to transfer money does not have enough money")
        account.amount -= amount
        self.amount += amount

    def deposit_to(self, account, amount):
        if account is not Account:
            raise ValueError("Need to pass in another Account")
        if account.get_amount < amount:
            raise ValueError("The Account to transfer money does not have enough money")
        account.amount -= amount
        self.amount += amount

    def take_from(self, income_source, amount):
        if type(income_source) is not IncomeSource:
            raise ValueError("Need to pass in a Resource of money")
        if income_source.amount < amount:
            raise ValueError("The Account to transfer money does not have enough money")
        income_source.amount -= amount
        self.amount += amount
