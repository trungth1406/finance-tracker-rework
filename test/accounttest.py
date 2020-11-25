import unittest

from account.resource import Account, IncomeSource


class AccountTest(unittest.TestCase):

    def test_init_account(self):
        account = Account(name="Saving Account", from_resource=None)
        self.assertEqual(account.get_remain_in_account, 0)

    def test_init_resource(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        self.assertIsNotNone(resource.get_amount)

    def test_with_draw(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        account = Account(name="Saving Account", from_resource=resource)
        account.withdraw_from_resource(5000000)
        self.assertEqual(account.get_remain_in_account, 5000000)
        self.assertEqual(resource.get_amount, 13000000)

    def test_withdraw_from_acc(self):
        resource = IncomeSource(name="Monthly salary", amount=18000000)
        account_1 = Account(name="Saving Account", from_resource=resource)
        account_2 = Account(name="Investing Account", from_resource=resource)
        account_1.withdraw_from_resource(1000000)
        account_2.withdraw_from_resource(2000000)
        self.assertEqual(account_1.get_remain_in_account, 1000000)
