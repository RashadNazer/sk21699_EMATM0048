# Part 1: Software Development

The software is a simple online banking system. To run the program, run **main.py**. There are two csv files in the directory. *bank.csv* file is used to store the user details and *tranasactions.csv* file is used to store transaction details.

To login as Admin, enter password: Sdpa@123
To login as Customer, you can use any of the user account data in the csv file. Here is a sample data: Account number = 1001006 and PIN = 6789

#### Classes in the program

The program has 4 classes. The classes and the functions in these classes are given below.

1. **customer_account class:**\
   This class reads the bank.csv file which has all the users details. The functions in this class are:
   
   - **welcome()**\
     This function displays the first main menu when the program is run. It gives the user 4 options to choose: *Login to account, Create account, Login as Admin and Shutdown.*
     
   - **login()**\
     This function verifies the credentials the user inputs and logs them in. If the account in frozen, user cannot log in to the system. This function also updates the balance of checking account holders by adding interest. This is done by calling update_balance().
    
   - **deposit()**\
      This function allows user to deposit money into the account. The user cannot enter negative values or other type of data in the field of deposit input.
      
   - **withdraw()**\
      This function allows user to withdraw money from the account. The user cannot enter negative values or other type of data in the field of deposit input. Fees for transaction, if any, is charged here. If balance is insufficient for withdrawl, function will print appropriate message.
      
   - **start_transfer()**\
      This function initiates money transfer after completing some checks. First it will check the recipient account number. It should not be their own account number. Also the account must be in the same bank. Secondly, the transfer amount should be less than 1000. If these checks are passed transfer() is called.
   - **change_pin()**\
      This function allows the user to change pin. The user cannot give account number as the new pin. Moreover, the new pin should satisfy the follwing conditions: *Atleast one number, Atleast one uppercase character, Atleast one lowercase character, Atleast one speacial character and be 6-10 characters long*
      
   - **menu()**\
       This function displays the main menu after the customer has logged in successfully. The menu displays the options for: *Deposit, Transfer, Withdraw, Change PIN, Transaction History, Freeze Account and Logout.*
  
2. **online_bank class:**\
    This class has customer_account class as its parent class. It inherits everything from customer_account class. The functions in this class are:
    
    - **admin()**\
        This function allows admin to see user details, see all transaction history details and also gives the option to change the freeze status of accounts.
    - **create_account()**\
        This function gives new users the option to create account. The user can select the type of account they want: Savings or Checking. The function generates a random PIN for the user. The user can change the PIN after logging in.
    - **transfer()**\
        This function process the tranfer between accounts after the pre-checks are completed by start_tranfer().
        
     - **transaction()**\
        This function saves the transaction details of the account into transactions.csv file. This function is called after every successful transaction has taken place. 
      
     - **logout()**\
        This functions logs out the user and directs them to the first menu, i.e. welcome().
        
     - **transaction_history()**\
        This function prints the transaction details of the user account by reading transactions.csv file.
     - **freeze()**\
        This function freezes the account of the user. Once the account is frozen, only the Admin can unfreeze the account.
        
 3. **savings_account class:**\
    This class is for savings account transactions. It has online_bank as its parent class. Only one function is present in this class: *withdraw()*, which assigns a flat transactional fee for each withdrawl and calls withdraw() to complete tranasction. The transaction fee is 5 per transaction.
  
 4. **checking_account class:**\
    This class is for checking account transactions. It has online_bank as its parent class. This class has 2 functions:
    
    - **withdraw()**\
        This functions initiates withdrawl by calling withdraw() and passes *0* as transactional fees. 
    - **update_balance()**\
        This function updates the balance of checking account by calculating interest for the period since the last updation of balance to current time. The annual interest rate is 5% and the interest is calculated on daily basis.
