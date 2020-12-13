import unittest
from datetime import date

from account.resource import Resource, Account
from account.transaction import ResourceTransaction


class TransactionTest(unittest.TestCase):

    def test_transaction(self):
        resource = Resource(name="Monthly salary", amount=18000000)
        account = resource.create_account(name="Saving Account", with_amount=5000000)
        transaction = ResourceTransaction(date_of_execution=None, from_resource=resource, to_resource=account)
        transaction.execute_deposit(amount=1000000)
        self.assertEqual(account.get_current_amount(), 6000000)
        self.assertEqual(resource.get_current_amount(), 12000000)
        self.assertEqual(transaction.get_date(), date.today())
        self.assertEqual(transaction.get_name(), "Transfer from Monthly salary to Saving Account")
