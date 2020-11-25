import unittest

from account.resource import Account, IncomeSource


class AccountTest(unittest.TestCase):

    def test_init_account(self):
        account = Account(name="Saving Account", limit=5000000)
        self.assertEqual(account.get_amount, 0)

    def test_init_resource(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        self.assertIsNotNone(resource.get_amount)

    def test_with_draw(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        account = Account(name="Saving Account", limit=5000000)
        account.take_from(resource, 5000000)
        self.assertEqual(account.get_amount, 5000000)
        self.assertEqual(resource.get_amount, 13000000)

