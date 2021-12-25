import csv
import re
from datetime import datetime
time = datetime.now()
current_time = time.strftime("%d-%m-%y %H:%M")


class customer_account:
    customer = open("bank.csv", "r")
    bank_csv = csv.reader(customer)
    bank_data = [row for row in bank_csv]
    customer.close()
    session_transaction = []
    

    def _init_(self, bank_data, session_transaction):
        self.bank_data = bank_data
        self.session_transaction = session_transaction
        

    def login(self):
        '''
        Login function that reads the bank.csv files in the depository and stores the details in a list.
        It also verifies the credentials the user inputs
        '''
        for row in self.bank_data:
            if row[4]=="Checking":
                acc_number=row[0]
                checking_account.update_balance(self, acc_number)
        
        found=0
        acc_number = input("Enter the Account Number: ")
        for row in self.bank_data:
            if acc_number == row[0]:
                found=1
                status=row[6]
                if status=='1':
                    print("Sorry. Your account is frozen. Please contact the nearest branch for further details.")
                    return
                pin = input("Enter your PIN: ")
                if pin == row[1]:
                    print("Login Succesful")
                    customer_account.menu(self, acc_number, self.bank_data)
                    break
                else:
                    print("Incorrect PIN")
                    break
        if found == 0:
            print("Account Not Found. Please Try again")
            customer_account.login(self)
                

    def deposit(self, acc_number):
        '''
        Function that deposits money into account
        '''
        print("Enter the amount to be deposited: ")
        amount = input()
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
        new_balance = int(current_balance)+int(amount)
        for row in self.bank_data:
            if acc_number == row[0]:
                row[3] = new_balance
        online_bank.transaction(
            self, acc_number, "Deposit", amount, new_balance)
        online_bank.update_csv(self)

    def withdraw(self, acc_number, transactional_fees):
        '''
        Function that withdraws amount from account.

        '''
        print("Enter the amount to be withdrawn: ")
        amount = input()
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
        new_balance = int(current_balance)-int(amount)+transactional_fees
        if int(current_balance) > int(amount):
            for row in self.bank_data:
                if acc_number == row[0]:
                    row[3] = new_balance
                    online_bank.transaction(self, acc_number, "Withdraw", amount, new_balance)
                    online_bank.update_csv(self)
        else:
            print("Insufficient Balance")

    def start_transfer(self, acc_number):
        '''
        Function that initiates transfer function.

    
        '''
        print("Enter the recipient account number: ")
        rec_number = input()
        if acc_number == rec_number:
            print("You cannot transfer into your own account")
        p = 0
        for row in self.bank_data:
            if rec_number == row[0]:
                print("Account found")
                p = 1
                rec_balance = row[3]
                print("Enter the amount to be transferred: ")
                amount = input()
                if(int(amount) <= 1000):
                    online_bank.transfer(self, acc_number, rec_number, rec_balance, amount)
                else:
                    print("Transfer to another account restricted to 1000. Please enter a valid amount.")
                    customer_account.start_transfer(self, acc_number)
        while(p != 1):
            print("Account not found")
            return

    def change_pin(self, acc_number):
        '''
        Function that changes PIN of user.
        '''
        print("""New PIN must have:
              1. Atleast one number
              2. Atleast one uppercase character
              3. Atleast one lowercase character
              4. Atleast one speacial character
              5. 6-10 characters long
              Enter the new PIN: """)
        new_pin = input()
        for row in self.bank_data:
            if acc_number == row[0]:
                if new_pin == row[1] or new_pin == row[0] or new_pin == row[2]:
                    print("You cannot enter current PIN or use your account number or name as PIN. ")
                    customer_account.change_pin(self, acc_number)
                else:
                    password_requirements = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
                    # compiling regex
                    password = re.compile(password_requirements)

                    # searching regex
                    status = re.search(password, new_pin)
                    if status:
                        for row in self.bank_data:
                            if acc_number == row[0]:
                                row[1] = new_pin
                                online_bank.update_csv(self)
                    else:
                        print("Invalid Password")
                        customer_account.change_pin(self, acc_number)

    def menu(self, acc_number, bank_data):
        '''
        Menu function that redirects user to appropriate function based on the input from user
        '''
        print("MENU".center(100))
        print("1. Deposit".center(100))
        print("2. Withdraw".center(100))
        print("3. Transfer".center(100))
        print("4. Change PIN".center(100))
        print("5. Transaction History".center(100))
        print("6. Freeze Account".center(100))
        print("7. Logout".center(100))
        print("Enter your choice= ")
        choice = input()
        if choice == '1':
            customer_account.deposit(self, acc_number)
        elif choice == '2':
            for row in bank_data:
                if row[0]==acc_number:
                    
                    if row[4]=="Savings":
                        savings_account.withdraw(self, acc_number)
                    else:
                        checking_account.withdraw(self, acc_number)
        elif choice == '3':
            customer_account.start_transfer(self, acc_number)
        elif choice == '4':
            customer_account.change_pin(self, acc_number)
        elif choice == '5':
            online_bank.transaction_history(self, acc_number)
        elif choice == '6':
            online_bank.freeze(self, acc_number)
        elif choice == '7':
            online_bank.logout(self, acc_number)   
        else:
            print("Invalid option")
            customer_account.menu(self, acc_number)


class online_bank(customer_account):
    '''
    Function that transfers money between accounts in the same bank
    '''
    
    
    def transfer(self, acc_number, rec_number, rec_balance, amount):
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
                if int(current_balance) > int(amount):
                    sender_balance = int(current_balance)-int(amount)
                    rec_balance = int(rec_balance)+int(amount)
                    row[3] = sender_balance
                    online_bank.transaction(self, acc_number, "Transfer Out", amount, sender_balance)
                    for row in self.bank_data:
                        if rec_number == row[0]:
                            row[3] = rec_balance
                            online_bank.transaction(self, rec_number, "Transfer IN", amount, rec_balance)
                            online_bank.update_csv(self)
                            return
                else:
                    print("Insufficient Balance")
                    return

    def transaction(self, acc_number, char, amount, new_balance):
        '''
        Function that records transaction details and store it in transaction.csv file

        '''
        this_transaction = [acc_number, char,amount, new_balance, current_time]
        self.session_transaction.extend(this_transaction)
        print(self.session_transaction)
        new_trans = open("transactions.csv", "a", newline="")
        update_trans = csv.writer(new_trans)
        update_trans.writerow(self.session_transaction)
        self.session_transaction.clear()

    def update_csv(self):
        '''
        Function that updates banks.csv file

        '''
        new_data = open("bank.csv", "w+", newline="")
        update_bank = csv.writer(new_data)
        for row in self.bank_data:
            update_bank.writerow(row)

    def logout(self, acc_number):
        '''
        Function that logs out the user from application
        '''
        print("Do you want to logout? (Y/N): ")
        answer = input()
        if(answer == "Y" or answer == "y"):
            customer_account.login(self)

        elif(answer == "N" or answer == "n"):
            customer_account.menu(self, acc_number)

        else:
            print("Enter a valid response")
            online_bank.logout(acc_number)

    def transaction_history(self, acc_number):
        '''
        Function that prints transaction history by reading transactions.csv
        '''
        history_print=[["Account Number","Transaction Type","Amount","Updated Balance","Time"]]
        history = open("transactions.csv", "r")
        trans_history = csv.reader(history)
        history_data = [row for row in trans_history]
        history.close()
        for row in history_data:
            if acc_number==row[0]:
                history_print.append(row)
        # Finding length of each row elements in history_print list
        length_history = [len(element) for row in history_print for element in row]
        # Setting longest length as column width
        column_width=max(length_history)
        # Printing transaction history in a table format
        for row in history_print:
            row = "".join(element.ljust(column_width + 2)for element in row)
            print(row)

    def calculate_interest(self, acc_number, rate):
        '''
        Function that calculates interest
        '''
        for row in self.bank_data:
            if row[0]==acc_number:
                last_updated=row[5]
                
                format="%d-%m-%y %H:%M"
                time_period=datetime.strptime(current_time , format) - datetime.strptime(last_updated , format)
                time_period = time_period.days
                
                interest_rate=time_period*rate
                current_balance=row[3]
                new_balance=float(current_balance)*(1+float(interest_rate))
                
                new_balance='%.2f'%new_balance
                row[3]=new_balance
                row[5]=current_time
                online_bank.update_csv(self)
    
    def freeze(self, acc_number):
        """
        Function that freeze the account of the user
        """
        print("Are you sure you want to freeze your account?")
        choice=input()
        if(choice == "Y" or choice == "y"):
            for row in self.bank_data:
                if row[0]==acc_number:
                    row[6]=1
                    online_bank.update_csv(self)
            
        elif(choice == "N" or choice == "n"):
            customer_account.menu(self, acc_number)

        else:
            print("Enter a valid response")
            online_bank.logout(acc_number)    
            
class savings_account(online_bank):
    
    """A bank account that charges for withdrawals."""
    
        
    def withdraw(self, acc_number):
        transactional_fees = 5
        customer_account.withdraw(self, acc_number, transactional_fees)
        
           
class checking_account(online_bank,customer_account):
    """
    A bank account that gives interest payments
    """
    
    def withdraw(self, acc_number):
        transactional_fees = 0
        customer_account.withdraw(self, acc_number, transactional_fees)
    
    def update_balance(self, acc_number):
        # Annual interest rate =5%
        # Daily interest rate =0.0137%
        interest_rate=0.000137
        for row in self.bank_data:
            if row[4]=="Checking":
                
                online_bank.calculate_interest(self, acc_number, interest_rate)
        

new_instance = customer_account()
new_instance.login()
