import csv



def login():
    '''
    Login function that reads the bank.csv files in the depository and stores the details in a list.
    It also verifies the credentials the user inputs
    '''
    customer=open("bank.csv","r")
    bank_csv=csv.reader(customer)
    header= next(bank_csv)
    bank_data=[row for row in bank_csv]
    print(header)
    print(bank_data)
    customer.close()
    
    
    acc_number= input("Enter the Account Number: ")
    
    for row in bank_data:
        if acc_number==row[0]:
            pin= input("Enter your PIN: ")
            if pin==row[1]:
                print("Login Succesful")
                menu()
                break
            else:
                print("Incorrect PIN")
                break
    

    
def menu():
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
        deposit()
        
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
