from datetime import datetime

class Expense:
    def __init__(self, amount, category, date=None):
        self._amount = amount
        self._category = category
        self._date = date if date else datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self._date}: ${self._amount} - {self._category}"

class RecurringExpense(Expense):
    def __init__(self, amount, category, frequency, date=None):
        super().__init__(amount, category, date)
        self._frequency = frequency

class ExpenseFactory:
    @staticmethod
    def create_expense(amount, category, date=None):
        return Expense(amount, category, date)

class FinanceTracker:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FinanceTracker, cls).__new__(cls)
            cls._instance._users = {}
            cls._instance._group_deposits = []
            cls._instance._expenses = []
            cls._instance._deposit_limits = {'daily': None, 'weekly': None, 'monthly': None}
        return cls._instance

    def add_user(self, user_id, name, account_number):
        self._users[user_id] = {'name': name, 'account_number': account_number, 'balance': 0}

    def add_group_deposit(self, deposit_amount, user_ids):
        valid_users = {uid: self._users[uid] for uid in user_ids if uid in self._users}
        if len(valid_users) == len(user_ids):
            for uid in user_ids:
                self._users[uid]['balance'] += deposit_amount
            self._group_deposits.append((deposit_amount, user_ids))
            print(f"Group deposit of ${deposit_amount} added for users {', '.join(user_ids)}.")
        else:
            missing = set(user_ids) - set(valid_users.keys())
            print(f"Deposit failed. No records for user IDs: {', '.join(missing)}.")

    def track_expense(self, expense):
        self._expenses.append(expense)

    def add_expense(self, amount, category, date=None):
        expense = ExpenseFactory.create_expense(amount, category, date)
        self.track_expense(expense)

    def remove_expense(self, expense):
        self._expenses.remove(expense)

    def print_expense_history(self):
        for expense in self._expenses:
            print(expense)

    def save_expense_history(self, filename):
        with open(filename, 'w') as file:
            for expense in self._expenses:
                file.write(str(expense) + "\n")

    def set_deposit_limit(self, period, limit):
        if period in self._deposit_limits:
            self._deposit_limits[period] = limit

    def print_user_info(self):
        for user_id, info in self._users.items():
            print(f"User {user_id}: {info['name']}, Account Number: {info['account_number']}, Balance: ${info['balance']}")

if __name__ == "__main__":
    tracker = FinanceTracker()

    # Interactively add users
    while True:
        user_id = input("Enter a new user ID (or type 'done' to finish adding users): ")
        if user_id.lower() == 'done':
            break
        name = input("Enter user's name: ")
        account_number = input("Enter user's account number: ")
        tracker.add_user(user_id, name, account_number)

    # Interactively add group deposits
    while True:
        decision = input("Would you like to add a group deposit? (yes/no): ")
        if decision.lower() == 'no':
            break
        deposit_amount = float(input("Enter the deposit amount: "))
        user_ids = input("Enter the user IDs to deposit to (comma-separated): ").split(',')
        tracker.add_group_deposit(deposit_amount, user_ids)

    # Add expenses
    tracker.add_expense(50, "Food")
    tracker.add_expense(30, "Transportation", "2024-04-20")

    # Print user and expense information
    tracker.print_user_info()
    print("Expense History:")
    tracker.print_expense_history()

    tracker.save_expense_history("expense_history.txt")
    tracker.set_deposit_limit('daily', 100)
    print("Deposit Limits:", tracker._deposit_limits)