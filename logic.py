from gui import Ui_MainWindow
import csv

#Make it easier to call the file name multiple times
FILE: str = "accounts.csv"

class Account:
    def __init__(self, first: str, last: str, pin: str, balance: float = 0.0) -> None:
        """
        Initialises the account object
        :param first: First name of the account holder
        :param last: Last name of the account holder
        param pin: PIN of the account
        :param balance: initial balance of the account holder
        """
        self.__first = first
        self.__last = last
        self.__pin = pin
        self.__balance = balance
    def get_name(self) -> str:
        """
        get the full name of the account holder
        :return:  full name as "First Last"
        """
        return f"{self.__first} {self.__last}"
    def get_balance(self) -> float:
        """
        get the balance of the account holder
        :return: Current balance
        """
        return self.__balance
    def verify_pin(self, pin: str) -> bool:
        """
        verify if a pin matches the account's pin
        :param pin: pin to verify
        :return: True if the pin matches the account's pin, false otherwise
        """
        return self.__pin == pin
    def deposit(self, amount: float) -> bool:
        """
        Deposit a positive amount into the account
        :param amount: amount to deposit
        :return:  True if the deposit was successful, false otherwise
        """
        if amount <= 0:
            return False
        self.__balance += amount
        return True
    def withdraw(self, amount: float) -> bool:
        """
        Withdraw a positive amount into the account
        :param amount: amount to withdraw
        :return: True if the withdrawal was successful, false otherwise
        """
        if amount <= 0 or amount > self.__balance:
            return False
        self.__balance -= amount
        return True
    def to_row(self) -> list[str]:
        """
        convert the data to a csv row
        :return: list of string values to represent the account
        """
        return [self.__first, self.__last, self.__pin ,str(self.__balance)]
    def from_row(row: list) -> "Account":
        """
        create an account instance from a csv row
        :param row: list of string values to represent the account        :return:  instance
        """
        return Account(row[0], row[1], row[2], float(row[3]))
class Logic:
    def __init__(self, ui: Ui_MainWindow) -> None:
        """
        Initialises the logic with the ui instance
        :param ui: the main window for the ui
        """
        self.ui = ui
        self.accounts = []
        self.current_account = None

        self.load_accounts()
        self.connect_buttons()
    def clear_all(self) -> None:
        """
        clears all inputs and messaged
        called when exit is pressed
        """
        self.ui.first_input.clear()
        self.ui.last_input.clear()
        self.ui.pin_input.clear()
        self.ui.login_message.clear()
        self.ui.amount_entered.clear()
        self.ui.amount_message.clear()
        self.ui.deposit.setChecked(True)
        self.ui.withdrawal.setChecked(False)
    def load_accounts(self) -> None:
        """
        load the accounts from the csv file
        if file does not exist, none are loaded
        """
        try:
            with open(FILE, "r") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    self.accounts.append(Account.from_row(row))
        except FileNotFoundError:
            pass

    def save_accounts(self) -> None:
        """
        save the accounts to the csv file
        overwrites existing file
        """
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            for account in self.accounts:
                writer.writerow(account.to_row())
    def connect_buttons(self) -> None:
        """
         connects the buttons to their logic methods
        """
        self.ui.create_account.clicked.connect(self.create_account)
        self.ui.login.clicked.connect(self.login_account)
        self.ui.enter.clicked.connect(self.process_transaction)
        self.ui.log_out.clicked.connect(self.logout)
    def create_account(self) -> None:
        """
        creates a new account using values from the input fields
        prevents a duplicate account and validates input
        """
        first = self.ui.first_input.text().strip()
        last = self.ui.last_input.text().strip()
        pin = self.ui.pin_input.text().strip()
        if not first or not last or not pin:
            self.ui.login_message.setText("Invalid input")
            return
        full_name = f"{first} {last}"
        for account in self.accounts:
            if account.get_name().lower() == full_name.lower():
                self.ui.login_message.setText("Account already exists")
                return
        new_account = Account(first, last, pin, 0.0)
        self.accounts.append(new_account)
        self.save_accounts()

        self.ui.login_message.setText("Account created")
    def login_account(self) -> None:
        """
        log in to an existing account
        enables the logged in frame on successful login
        prevents a second login unless the person exits the atm
        """
        if self.current_account:
            self.ui.login_message.setText("Already Logged in.")
            return
        first = self.ui.first_input.text().strip()
        last = self.ui.last_input.text().strip()
        pin = self.ui.pin_input.text().strip()

        full_name = f"{first} {last}"
        for account in self.accounts:
            if account.get_name().lower() == full_name.lower():
                if account.verify_pin(pin):
                    self.current_account = account
                    self.ui.logged_in.setEnabled(True)
                    self.ui.login_message.setText(f"Welcome {account.get_name()}")
                    return
        self.ui.login_message.setText("Invalid login")
    def process_transaction(self) -> None:
        """
        process a deposit or withdrawal based on the selected radio button
        updates balance and displays results
        """
        if self.current_account is None:
            return
        try:
            amount = float(self.ui.amount_entered.text())
            amount = float(f"{amount:.2f}")
        except ValueError:
            self.ui.amount_message.setText("Enter a valid number")
            return
        if self.ui.deposit.isChecked():
            success = self.current_account.deposit(amount)
        else:
            success = self.current_account.withdraw(amount)
        if success:
            self.save_accounts()
            self.ui.amount_message.setText(f"Success! New balance: ${self.current_account.get_balance():.2f}")
        else:
            self.ui.amount_message.setText("Transaction failed")
    def logout(self) -> None:
        """
        Log out the current account, disables the frame and clears input and messages
        """
        self.current_account = None
        self.ui.logged_in.setEnabled(False)
        self.clear_all()
        

