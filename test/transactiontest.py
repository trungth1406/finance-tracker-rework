import unittest
from datetime import date

from account.resource import IncomeSource, Account
from account.transaction import AccountTransaction


class TransactionTest(unittest.TestCase):

    def test_transaction(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        account = resource.create_account(name="Saving Account", with_amount=5000000)
        transaction = AccountTransaction(date_of_execution=None, from_acc=account)
        transaction.withdraw_from(from_source=resource, amount=1000000)
        self.assertEqual(account.amount, 6000000)
        self.assertEqual(resource.get_amount, 12000000)
        self.assertEqual(transaction.get_date(), date.today())
