import csv
from datetime import datetime
time=datetime.now()
current_time=time.strftime("%d/%m/%y %H:%M:%S")

customer=open("bank.csv","r")
bank_csv=csv.reader(customer)
bank_data=[row for row in bank_csv]
customer.close()
session_transaction=[]

def login():
    '''
    Login function that reads the bank.csv files in the depository and stores the details in a list.
    It also verifies the credentials the user inputs
    '''
    
    
    acc_number= input("Enter the Account Number: ")
    
    for row in bank_data:
        if acc_number==row[0]:
            pin= input("Enter your PIN: ")
            if pin==row[1]:
                print("Login Succesful")
                menu(acc_number)
                break
            else:
                print("Incorrect PIN")
                break
    
def deposit(acc_number):
    '''
    Function that deposits money into account
    '''
    print("Enter the amount to be deposited: ")
    amount=input()
    for row in bank_data:
        if acc_number==row[0]:
            current_balance=row[3]
    new_balance=int(current_balance)+int(amount)
    for row in bank_data:
        if acc_number==row[0]:
            row[3]=new_balance
    transaction(acc_number, "Deposit", amount, new_balance)
    update_csv(bank_data)

def withdraw(acc_number):
    '''
    Function that withdraws amount from account.

    '''
    print("Enter the amount to be withdrawn: ")
    amount=input()
    for row in bank_data:
        if acc_number==row[0]:
            current_balance=row[3]
    new_balance=int(current_balance)-int(amount)
    if int(cur)<0:
        
        for row in bank_data:
            if acc_number==row[3]:
                row[3]=new_balance
    else:
        print("Insufficient Balance")
    transaction(acc_number, "Withdraw", amount, new_balance)
    update_csv(bank_data)
    
    
def transaction(acc_number, char, amount, new_balance):
    '''
    Function that records transaction details and store it in transaction.csv file

    '''
    this_transaction=[acc_number, char ,amount, new_balance, current_time]
    session_transaction.extend(this_transaction)
    print(session_transaction)
    new_trans=open("transactions.csv","a", newline="")
    update_trans=csv.writer(new_trans)
    update_trans.writerow(session_transaction)
    
def update_csv(bank_data):
    '''
    Function that updates banks.csv file

    '''
    new_data=open("bank.csv","w+",newline="")
    update_bank=csv.writer(new_data)
    for row in bank_data:
        update_bank.writerow(row)


def menu(acc_number):
    '''
    Function that displays menu and redirects the user to appropriate function based on the user's input

    '''
    print("MENU".center(100))
    print("1. Deposit".center(100))
    print("2. Withdraw".center(100))
    print("3. Transfer".center(100))
    print("4. Logout".center(100))
    print("Enter your choice= ")
    choice= input()
    if choice == '1':
        deposit(acc_number)
        
    elif choice== '2':
        withdraw(acc_number)
    
    elif choice =='3':
        transfer()
        
    elif choice == '4':
        login()
        
    else:
        print("Invalid option")
        menu()





login()
