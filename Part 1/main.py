import csv
import datetime
today=datetime.date.today()


customer=open("bank.csv","r")
bank_csv=csv.reader(customer)
header= next(bank_csv)
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
    transaction(acc_number, "Deposit", amount)
    
def transaction(acc_number, char, amount):
    '''
    Function that records transaction details and store it in transaction.csv file

    '''
    time=today.ctime()
    this_transaction=[acc_number,char,amount,time]
    session_transaction.extend(this_transaction)
    print(session_transaction)
    
    


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
        withdraw()
    
    elif choice =='3':
        transfer()
        
    elif choice == '4':
        login()
        
    else:
        print("Invalid option")
        menu()





login()
