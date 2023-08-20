import holder
import unittest


class BankTest(unittest.TestCase):

    def test_create_bank(self):
        bank = holder.Bank(50000)
        self.assertEqual(bank.budget, 50000)


if __name__ == '__main__':
    unittest.main()