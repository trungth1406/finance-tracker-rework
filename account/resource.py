from abc import ABC


class Transferable(ABC):

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def get_name(self):
        return self.name

    def deposit(self, amount):
        self.amount += amount
        return self

    def withdraw(self, amount):
        if amount > self.amount:
            raise ValueError("Insufficient amount")
        self.amount -= amount
        return self

    def transfer_to(self, transferable, with_amount):
        self.withdraw(with_amount)
        transferable.deposit(with_amount)

    def withdraw_from(self, transferable, with_amount):
        self.deposit(with_amount)
        transferable.withdraw(with_amount)

    def get_current_amount(self):
        return self.amount


class Resource(Transferable):

    def create_account(self, name, with_amount):
        account = Account(name=name, amount=0, from_resource=self)
        account.withdraw_from_resource(with_amount)
        return account


class Account(Transferable):

    def __init__(self, name, amount, from_resource):
        super().__init__(name, amount)
        self.from_resource = from_resource

    @classmethod
    def init_from_resource(cls, name, resource):
        return cls(name, resource)

    def withdraw_from_resource(self, amount):
        self.from_resource.withdraw(amount)
        self.deposit(amount)

    def return_to_resource(self):
        self.withdraw(self.amount)
        self.from_resource.deposit(self.amount)
