from abc import ABC, abstractmethod
from datetime import date

from account.resource import Transferable


class Transactional(ABC):

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_date(self):
        pass

    @abstractmethod
    def get_transaction_amount(self):
        pass


class BaseTransaction(Transactional):

    def __init__(self, date_of_execution):
        self.name = ""
        self.date = date_of_execution
        self.transaction_amount = 0

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date if self.date is not None else date.today()

    def get_transaction_amount(self):
        return self.transaction_amount


class ResourceTransaction(BaseTransaction):

    def __init__(self, date_of_execution, from_resource: Transferable, to_resource: Transferable):
        super().__init__(date_of_execution)
        if issubclass(type(to_resource), Transferable):
            self.to_resource = to_resource
        if issubclass(type(from_resource), Transferable):
            self.from_resource = from_resource

    def get_name(self):
        self.name = f'Transfer from {self.from_resource.get_name()} to {self.to_resource.get_name()}'
        return self.name

    def execute_deposit(self, amount):
        self.transaction_amount = amount
        self.from_resource.transfer_to(self.to_resource, amount)
        return self

    def execute_withdraw(self, amount):
        self.transaction_amount = amount
        self.from_resource.withdraw_from(self.to_resource, amount)
        return self
