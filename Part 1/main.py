import csv
import re
import sys
import numpy as np
import pandas as pd
from random import randint
from datetime import datetime
import time as delay
time = datetime.now()
current_time = time.strftime("%d-%m-%y %H:%M")


class customer_account:
    #Read bank.csv file and store the data
    customer = open("bank.csv", "r")
    bank_csv = csv.reader(customer)
    bank_data = [row for row in bank_csv]
    customer.close()
    session_transaction = []
    

    def _init_(self, bank_data, session_transaction):
        self.bank_data = bank_data
        self.session_transaction = session_transaction
        
    def welcome(self):
        '''
        Menu function thats show 4 main options and redirects user accordingly

        '''
        customer = open("bank.csv", "r")
        bank_csv = csv.reader(customer)
        self.bank_data = [row for row in bank_csv]
        customer.close()
        print("\n")
        print("Welcome to The Bank".center(100))
        print("Please select your option".center(100))
        print("1. Login to account")
        print("2. Create account")
        print("3. Admin Login")
        print("4. Shutdown")
        choice=input()

        if choice == '1':
            customer_account.login(self)
            
        elif choice == '2':
            online_bank.create_account(self)
            
        elif choice == '3':
            print("Enter password: ")
            password=input()
            if password=='Sdpa@123':
                online_bank.admin(self)
                
        elif choice == '4':
            sys.exit()
        
        else:
            print("Invalid option")
            delay.sleep(2)
            customer_account.welcome(self)


    def login(self):
        '''
        Login function verifies the credentials the user inputs. This function also checks the freeze status of user and restricts the user if thei account id frozen.
        
        '''
        # Update balance of checking account holders by calling update_balance()
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
                #Checking Freeze Status
                if status=='1':
                    print("Sorry. Your account is frozen. Please contact the nearest branch for further details.")
                    customer_account.welcome(self)
                    return
                pin = input("Enter your PIN: ")
                if pin == row[1]:
                    print("Login Succesful")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
                    break
                else:
                    print("Incorrect PIN. Please try again")
                    delay.sleep(2)
                    customer_account.welcome(self)
        if found == 0:
            print("Account Not Found or Invalid Data. Please Try again")
            delay.sleep(2)
            customer_account.welcome(self)
                

    def deposit(self, acc_number):
        '''
        Function that deposits money into account
        '''
        try:
            amount = float(input("Enter the amount to be deposited: "))
        except ValueError:
            print("You must enter a valid number.")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
        if amount<0:
            print("You must enter a valid number.")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
        #Updating balance 
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
                new_balance = float(current_balance) + float(amount)
                row[3] = new_balance
        #Saving transaction
        online_bank.transaction(self, acc_number, "Deposit", amount, new_balance)
        bank_df = pd.DataFrame(self.bank_data)
        bank_df.to_csv('bank.csv', index=False, header=False)
        print("Amount Deposited Successfully")
        delay.sleep(2)
        customer_account.menu(self, acc_number)

    def withdraw(self, acc_number, transactional_fees):
        '''
        Function that withdraws amount from account.

        '''
        try:
            amount = float(input("Enter the amount to withdraw: "))
        except ValueError:
            print("You must enter a valid number.")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
        if amount<0:
            print("You must enter a valid number.")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
        new_balance = float(current_balance)-float(amount)-transactional_fees
        #Checking if the account has sufficient balance
        if float(current_balance) > float(amount):
            for row in self.bank_data:
                if acc_number == row[0]:
                    row[3] = new_balance
                    #Updating balance
                    online_bank.transaction(self, acc_number, "Withdraw", amount, new_balance)
                    bank_df = pd.DataFrame(self.bank_data)
                    bank_df.to_csv('bank.csv', index=False, header=False)
                    print("Amount Withdrawn Successfully")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
        else:
            print("Insufficient Balance")
            delay.sleep(2)
            customer_account.menu(self, acc_number)

    def start_transfer(self, acc_number):
        '''
        Function that initiates transfer function. The user cannot transfer money to its own account. 
        Transfer also restricted to 1000.
        '''
        print("Enter the recipient account number: ")
        rec_number = input()
        amount=10000
        
        if acc_number == rec_number:
            print("You cannot transfer into your own account.")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
        p = 0
        for row in self.bank_data:
            if rec_number == row[0]:
                print("Account found")
                p = 1
                rec_balance = row[3]
                #Getting input from user
                try:
                    amount = float(input("Enter the amount to be transferred: "))
                except ValueError:
                    print("You must enter a valid number.")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
                if amount < 0:
                    print("You must enter a valid number.")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
                if(float(amount) <= 1000):
                    online_bank.transfer(self, acc_number, rec_number, rec_balance, amount)
                else:
                    print("Transfer to another account restricted to 1000. Please enter a valid amount.")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
        while(p != 1):
            print("Account not found")
            delay.sleep(2)
            customer_account.menu(self, acc_number)
            

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
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
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
                                bank_df = pd.DataFrame(self.bank_data)
                                bank_df.to_csv('bank.csv', index=False, header=False)
                                print("Password Changed Successfully")
                                delay.sleep(2)
                                customer_account.menu(self, acc_number)
                    else:
                        print("Invalid Password")
                        delay.sleep(2)
                        customer_account.menu(self, acc_number)

    def menu(self, acc_number):
        '''
        Menu function that redirects user to appropriate function based on the input from user
        '''
        print("\n")
        print("Welcome to The Bank".center(100))
        print("MENU".center(100))
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Transfer")
        print("4. Change PIN")
        print("5. Transaction History")
        print("6. Freeze Account")
        print("7. Logout")
        print("Enter your choice= ")
        choice = input()
        if choice == '1':
            customer_account.deposit(self, acc_number)
        elif choice == '2':
            for row in self.bank_data:
                if row[0]==acc_number:
                    #Redirecting user to withdraw() according to account type
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
            delay.sleep(2)
            customer_account.menu(self, acc_number)


class online_bank(customer_account):
    
    def admin(self):
        '''
        Admin function that shows user and transaction details. Also lets change freeze status of account
        '''
        print("\n")
        print("Welcome to The Bank".center(100))
        print("MENU".center(100))
        print("1. Show User details".center(100))
        print("2. Show transaction details".center(100))
        print("3. Change Freeze Status".center(100))
        print("4. Logout".center(100))
        print("Enter your choice= ")
        choice = input()
        if choice == '1':
            #Printing user details
            user_info = open("bank.csv", "r")
            user_csv = csv.reader(user_info)
            print_data = [row for row in user_csv]
            user_info.close()
            
            for row in print_data:
                del row[1]
            width=max(len(x) for l in print_data for x in l)  
            for row in print_data:
                print("".join(x.ljust(width+2) for x in row))
                
            online_bank.admin(self)
        elif choice == '2':
            #Printing transaction history
            history = open("transactions.csv", "r")
            trans_history = csv.reader(history)
            history_data = [row for row in trans_history]
            history.close()
            width=max(len(x) for l in history_data for x in l)
            
            for row in history_data:
                print("".join(x.ljust(width+2) for x in row))
            online_bank.admin(self)
            
        elif choice == '3':
            #Changing frozen status
            print("Enter the account number to be frozen/unfrozen: ")
            acc_number=input()
            print("Enter the action to be taken: Freeze(F)/Unfreeze(U) ")
            status=input()
            if status.lower() == 'f' or status.lower() == 'F':
                freeze_status=1
            elif status.lower() == 'u' or status.lower() == 'U':
                freeze_status=0  
            else:
                print("Invalid option")
                delay.sleep(2)
                online_bank.admin(self)
            p = 0
            for row in self.bank_data:
                if row[0] == acc_number:
                    row[6]=freeze_status
                    bank_df = pd.DataFrame(self.bank_data)
                    bank_df.to_csv('bank.csv', index=False, header=False)
                    print("Freeze status changed successfully")
                    delay.sleep(2)
                    online_bank.admin(self)
            while(p != 1):
                print("Account not found")
                delay.sleep(2)
                online_bank.admin(self)
        elif choice == '4':
            customer_account.welcome(self)
        else:
            print("Invalid option")
            delay.sleep(2)
            online_bank.admin(self)
            
            
            
            
    
    def create_account(self):
        '''
        Function that creates account
        '''
        print("Please enter your Name: ")
        name=input()
        #Getting account type from user
        print("Enter the type of account: Savings(S) or Checking(C)")
        account_type=input()
        if account_type.lower() == 's':
            account='Savings'
        elif account_type.lower() == 'c':
            account='Checking'   
        else:
            print("Invalid option")
            delay.sleep(2)
            online_bank.create_account(self)
        #Assigning a random PIN
        pin=randint(1000, 9999)
        array = np.array(self.bank_data)
        index = array.shape[0]
        #Assinging account number
        acc_number = 1001000 + index
        status=0
        balance=0
        new_account=[acc_number,pin,name,balance,account,current_time,status]
        #Saving details into bank.csv
        new_acc=open("bank.csv","a", newline="")
        update_bank=csv.writer(new_acc)
        update_bank.writerow(new_account)
        new_acc.close()
        new_account.clear()
        print("Bank account created successfully. Your account number is "+ str(acc_number))
        print("Your PIN is "+ str(pin))
        print("Please change your PIN after logging in.")
        delay.sleep(2)
        customer_account.welcome(self)
    
    def transfer(self, acc_number, rec_number, rec_balance, amount):
        '''
        Function that transfers money between accounts in the same bank
        '''
        for row in self.bank_data:
            if acc_number == row[0]:
                current_balance = row[3]
                if float(current_balance) > float(amount):
                    sender_balance = float(current_balance)-float(amount)
                    rec_balance = float(rec_balance)+float(amount)
                    row[3] = sender_balance
                    online_bank.transaction(self, acc_number, "Transfer Out", amount, sender_balance)
                    for row in self.bank_data:
                        if rec_number == row[0]:
                            row[3] = rec_balance
                            online_bank.transaction(self, rec_number, "Transfer IN", amount, rec_balance)
                            bank_df = pd.DataFrame(self.bank_data)
                            bank_df.to_csv('bank.csv', index=False, header=False)
                            print("Transfer Successful")
                            delay.sleep(2)
                            customer_account.menu(self, acc_number)
                            return
                else:
                    print("Insufficient Balance")
                    delay.sleep(2)
                    customer_account.menu(self, acc_number)
                    return

    def transaction(self, acc_number, char, amount, new_balance):
        '''
        Function that records transaction details and store it in transaction.csv file

        '''
        this_transaction = [acc_number, char,amount, new_balance, current_time]
        self.session_transaction.extend(this_transaction)
        new_trans = open("transactions.csv", "a", newline="")
        update_trans = csv.writer(new_trans)
        update_trans.writerow(self.session_transaction)
        self.session_transaction.clear()

        
    def logout(self, acc_number):
        '''
        Function that logs out the user from application
        '''
        print("Do you want to logout? (Y/N): ")
        answer = input()
        if(answer == "Y" or answer == "y"):
            customer_account.welcome(self)

        elif(answer == "N" or answer == "n"):
            customer_account.menu(self, acc_number)

        else:
            print("Enter a valid response")
            delay.sleep(2)
            online_bank.logout(self,acc_number)

    def transaction_history(self, acc_number):
        '''
        Function that records transaction details and store it in transaction.csv file

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
        delay.sleep(2)
        customer_account.menu(self, acc_number)

   
    
    def freeze(self, acc_number):
        """
        Function that freeze the account of the user
        """
        print("Are you sure you want to freeze your account?(Y/N)")
        choice=input()
        if(choice == "Y" or choice == "y"):
            for row in self.bank_data:
                if row[0]==acc_number:
                    row[6]=1
                    bank_df = pd.DataFrame(self.bank_data)
                    bank_df.to_csv('bank.csv', index=False, header=False)
                    print("Account Frozen Sucessfully. To unfreeze account, contact your Bank Administrator")
                    delay.sleep(2)
                    customer_account.welcome(self)
            
        elif(choice == "N" or choice == "n"):
            customer_account.menu(self, acc_number)

        else:
            print("Enter a valid response")
            delay.sleep(2)
            online_bank.logout(acc_number)    
            
class savings_account(online_bank):
    
    """A bank account that charges for withdrawals."""
    
        
    def withdraw(self, acc_number):
        """
        Function that assigns transactional fees and passes to withdraw()
        """
        transactional_fees = 5
        customer_account.withdraw(self, acc_number, transactional_fees)
        
           
class checking_account(online_bank,customer_account):
    """
    A bank account that gives interest payments
    """
    
    def withdraw(self, acc_number):
        """
        Function that assigns transactional fees and passes to withdraw()
        """
        transactional_fees = 0
        customer_account.withdraw(self, acc_number, transactional_fees)
    
    def update_balance(self, acc_number):
        """
        Function that passes interest rate to calculate_interest()

        """
        # Annual interest rate =5%
        # Daily interest rate =0.0137%
        interest_rate=0.000137
        for row in self.bank_data:
            if row[0]==acc_number:
                last_updated=row[5]
                
                format="%d-%m-%y %H:%M"
                #Calculating time since last update
                time_period=datetime.strptime(current_time , format) - datetime.strptime(last_updated , format)
                time_period = time_period.days
                #calculating the interest for the period from last update
                rate = time_period * interest_rate
                current_balance=row[3]
                new_balance=float(current_balance)*(1+float(rate))
                #Updating balance and time
                new_balance='%.2f'%new_balance
                row[3]=new_balance
                row[5]=current_time
                bank_df = pd.DataFrame(self.bank_data)
                bank_df.to_csv('bank.csv', index=False, header=False)
        

new_instance = customer_account()
new_instance.welcome()


    



