from datetime import datetime

class Expense:
    """Represents a single expense entry."""

    def __init__(self, amount, category, date=None):
        self._amount = amount
        self._category = category
        self._date = date if date else datetime.now().strftime("%Y-%m-%d")

    def __str__(self):
        return f"{self._date}: ${self._amount} - {self._category}"

class RecurringExpense(Expense):
    """Represents a recurring expense entry, inheriting from Expense."""

    def __init__(self, amount, category, frequency, date=None):
        super().__init__(amount, category, date)
        self._frequency = frequency

class ExpenseFactory:
    """Factory class to create expense instances."""

    @staticmethod
    def create_expense(amount, category, date=None):
        return Expense(amount, category, date)

class FinanceTracker:
    """Singleton class to track user finances, including users, deposits, and expenses."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FinanceTracker, cls).__new__(cls)
            cls._instance._users = {}
            cls._instance._group_deposits = []
            cls._instance._deposit_limits = {'daily': None, 'weekly': None, 'monthly': None}
        return cls._instance

    def add_user(self, user_id, name, account_number):
        """Adds a new user to the finance tracker."""
        user_id = user_id.lower()
        if user_id in self._users:
            print(f"User ID {user_id} already exists.")
        else:
            self._users[user_id] = {'name': name, 'account_number': account_number, 'balance': 0, 'expenses': []}
            print(f"User {name} added with ID {user_id}.")
            print(f"Current users: {list(self._users.keys())}")

    def add_group_deposit(self, deposit_amount, user_ids):
        """Adds a group deposit to specified users' balances."""
        user_ids = [uid.lower() for uid in user_ids]
        valid_users = {uid: self._users[uid] for uid in user_ids if uid in self._users}
        if len(valid_users) == len(user_ids):
            for uid in user_ids:
                self._users[uid]['balance'] += deposit_amount
            self._group_deposits.append((deposit_amount, user_ids))
            print(f"Group deposit of ${deposit_amount} added for users {', '.join(user_ids)}.")
        else:
            missing = set(user_ids) - set(valid_users.keys())
            print(f"Deposit failed. No records for user IDs: {', '.join(missing)}.")

    def add_expense(self, user_id, amount, category, date=None):
        """Adds an expense for a specific user."""
        user_id = user_id.lower()
        if user_id in self._users:
            expense = ExpenseFactory.create_expense(amount, category, date)
            self._users[user_id]['expenses'].append(expense)
        else:
            print(f"User ID {user_id} not found.")

    def remove_expense(self, user_id, expense):
        """Removes a specific expense from a user's expense list."""
        user_id = user_id.lower()
        if user_id in self._users:
            if expense in self._users[user_id]['expenses']:
                self._users[user_id]['expenses'].remove(expense)
            else:
                print(f"Expense not found for user ID {user_id}.")
        else:
            print(f"User ID {user_id} not found.")

    def print_expense_history(self, user_id):
        """Prints the expense history for a specific user."""
        user_id = user_id.lower()
        if user_id in self._users:
            print(f"Expense history for {self._users[user_id]['name']}:")
            for expense in self._users[user_id]['expenses']:
                print(expense)
        else:
            print(f"User ID {user_id} not found.")

    def save_expense_history(self, user_id, filename):
        """Saves the expense history of a specific user to a file."""
        user_id = user_id.lower()
        if user_id in self._users:
            with open(filename, 'w') as file:
                for expense in self._users[user_id]['expenses']:
                    file.write(str(expense) + "\n")
        else:
            print(f"User ID {user_id} not found.")

    def set_deposit_limit(self, period, limit):
        """Sets a deposit limit for a specified period."""
        if period in self._deposit_limits:
            self._deposit_limits[period] = limit

    def print_user_info(self):
        """Prints information about all users."""
        for user_id, info in self._users.items():
            print(f"User {user_id}: {info['name']}, Account Number: {info['account_number']}, Balance: ${info['balance']}")

def add_users(tracker):
    """Interactively adds users to the finance tracker."""
    while True:
        user_id = input("Enter a new user ID (or type 'done' to finish adding users): ")
        if user_id.lower() == 'done':
            break
        name = input("Enter user's name: ")
        account_number = input("Enter user's account number: ")
        tracker.add_user(user_id, name, account_number)

def add_group_deposits(tracker):
    """Interactively adds group deposits to the finance tracker."""
    while True:
        decision = input("Would you like to add a group deposit? (yes/no): ")
        if decision.lower() == 'no':
            break
        deposit_amount = float(input("Enter the deposit amount: "))
        user_ids = input("Enter the user IDs to deposit to (comma-separated): ").split(',')
        tracker.add_group_deposit(deposit_amount, user_ids)

def add_expenses(tracker):
    """Interactively adds expenses for users to the finance tracker."""
    while True:
        decision = input("Would you like to add an expense? (yes/no): ")
        if decision.lower() == 'no':
            break
        user_id = input("Enter the user ID: ")
        amount = float(input("Enter the expense amount: "))
        category = input("Enter the expense category: ")
        date = input("Enter the date of the expense (YYYY-MM-DD) or leave blank for today: ")
        date = date if date else None
        tracker.add_expense(user_id, amount, category, date)

if __name__ == "__main__":
    tracker = FinanceTracker()

    # Interactively add users
    add_users(tracker)

    # Interactively add group deposits
    add_group_deposits(tracker)

    # Interactively add expenses
    add_expenses(tracker)

    # Print user and expense information
    tracker.print_user_info()
    print("Expense History:")
    for user_id in tracker._users:
        tracker.print_expense_history(user_id)

    # Save expense history for users
    for user_id in tracker._users:
        filename = f"expense_history_{user_id}.txt"
        tracker.save_expense_history(user_id, filename)

    tracker.set_deposit_limit('daily', 100, )
    print("Deposit Limits:", tracker._deposit_limits)
