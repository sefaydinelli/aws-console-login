#!/usr/bin/python3
from selenium.webdriver.common.by import By
from selenium import webdriver
from tinydb import TinyDB, Query
from getpass import getpass
import argparse, time, os

parser = argparse.ArgumentParser()

home_dir = os.getenv("HOME")
db_dir = home_dir + "/.awsl"


# login to aws account with webdriver
def login_to_aws_account(account_name):
    try:
        aws_account_name = db.search(Query().acc_name == f'{account_name}')
        print(aws_account_name[0]['acc_name'])
        browser.get(url=f"{aws_account_name[0]['url']}")
        browser.maximize_window()
        username = browser.find_element(By.ID, "username")
        password = browser.find_element(By.ID, "password")
        username.send_keys(f"{aws_account_name[0]['username']}")
        password.send_keys(f"{aws_account_name[0]['password']}")
        login = browser.find_element(By.ID, "signin_button")
        login.click()
        return("Login success.")
    except:
        return("Login failed.")

def login_to_aws_account_with_mfa(account_name, mfa):
    try:
        aws_account_name = db.search(Query().acc_name == f'{account_name}')
        print(aws_account_name[0]['acc_name'])
        browser.get(url=f"{aws_account_name[0]['url']}")
        browser.maximize_window()
        username = browser.find_element(By.ID, "username")
        password = browser.find_element(By.ID, "password")
        username.send_keys(f"{aws_account_name[0]['username']}")
        password.send_keys(f"{aws_account_name[0]['password']}")
        login = browser.find_element(By.ID, "signin_button")
        login.click()
        time.sleep(2)
        mfacode = browser.find_element(By.ID, "mfacode")
        mfacode.send_keys(f"{mfa}")
        submit = browser.find_element(By.ID, "submitMfa_button")
        submit.click()
        return("Login success.")
    except:
        return("Login failed.")

# add new account to db
def instert_aws_acc_to_db(account_name):
    url = input("Enter the AWS Login URL : ")
    username = input("Enter username : ")
    password = getpass("Enter password : ")
    try:
        db.insert(
                {
                    'acc_name':f'{account_name}',
                    'url':f'{url}',
                    'username': f'{username}',
                    'password': f'{password}',
                }
            )
        return(f"Credentials succesfully inserted : {account_name}")
    except:
        return("Credentials couldn't inserted to DB.")

def delete_aws_acc_from_db(account_name):
    try:
        db.remove(Query().acc_name == account_name)
        print(f"{account_name} successfuly removed.")
    except:
        print(f"{account_name} couldn't removed.")

# insert new password to db
def change_password_from_db(account_name):
    try:
        if account_name in (db.search(Query().acc_name == f'{account_name}')[0]['acc_name']):
            new_pass = getpass(f"Enter new password for {account_name} : ")
            db.update({'password': f'{new_pass}'}, Query().acc_name == f'{account_name}')
            db.all()
            print (f"Password succesfuly changed for {account_name} . ")
        else:
            print(f"There is no account named {account_name} ...")
    except:
        print(f"There is no account named {account_name} ...")

def list_accounts_from_db():
    accounts = [r['acc_name'] for r in db]
    return accounts

if __name__ == "__main__":

    if not (os.path.exists(db_dir)):
        mkdir = os.system("mkdir -p {}".format(db_dir))

    db = TinyDB( db_dir + '/db.json')

    parser.add_argument('-m', '--mfa' ,type=int, required=False, help="Login with MFA code.")
    parser.add_argument('-a', '--add' ,type=str, required=False, help="Add new account.")
    parser.add_argument('-r', '--remove' ,type=str, required=False, help="Remove an account with account name")
    parser.add_argument('-u', '--update' ,type=str, required=False, help="Change password for existing account.")
    parser.add_argument("login" , nargs="?", help="Login to selected account, awsl <aws_acc>")
    args = parser.parse_args()


    if (args.add):
        instert_aws_acc_to_db(account_name=args.add)
    elif (args.update):
        change_password_from_db(account_name=args.update)
    elif (args.mfa):
        browser = webdriver.Chrome()
        login_to_aws_account_with_mfa(account_name=args.login, mfa=args.mfa)
    elif (args.remove):
        delete_aws_acc_from_db(account_name=args.remove)
    elif (args.login) == None:
        print(list_accounts_from_db())
    elif (args.login):
        browser = webdriver.Chrome()
        login_to_aws_account(account_name=args.login)
    else:
        print("ERROR WIP")
        
