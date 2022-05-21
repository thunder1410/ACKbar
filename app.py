#!/usr/bin/python
from models import Base, User, Product, Font
from sqlalchemy import func
from database import Session, engine
import os, time
from colorama import Fore, Style

# Testing visual studio code config... 4

clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

def succes(s):
    return Fore.GREEN + s + Style.RESET_ALL

def question(s):
    return Style.BRIGHT + s + Style.RESET_ALL

def info(s):
    return Style.DIM + s + Style.RESET_ALL

def warning(s):
    return Fore.YELLOW + s + Style.RESET_ALL

def error(s):
    return Fore.RED + s + Style.RESET_ALL


def logo(font):
    clearConsole()
    if font is None:
        print("ACKbar with font issues")
    else:
        os.system(f"figlet -t -f {font.name} ACKbar | lolcat")

def input_yesno(q):
    while True:
        answer = input(question(f"{q} y/n: ")).lower()
        if answer == "y" or answer == "yes":
            return "y"
        if answer == "n" or answer == "no":
            return "n"

def input_deposit():
    full = 0
    cents = 0
    isValid = False
    while not isValid:
        raw_money = input(question("How much money do you want to deposit: "))
        if "." in raw_money and len(raw_money.split(".")) == 2:
            try:
                full = int(raw_money.split(".")[0])
                cents = int(raw_money.split(".")[1])
            except:
                pass
            else:
                if full >= 0 and cents >= 0:
                    isValid = True
        else:
            try:
                full = int(raw_money)
            except:
                pass
            else:
                if full >= 0:
                    isValid = True
    money = full * 100 + cents
    return money

def purchaseScreen(users, products, deposit, total, font):
    logo(font)
    print("")
    print(f"Hello {users[0].name}, you have {(users[0].balance/100):.2f} on your account.")
    print(f"")
    print(info("Commands:"))
    print(info(" (A)ccept transaction"))
    print(info(" (C)ancel transaction"))
    print(info(" (D)eposit"))
    print("")
    print(f"{'balance' : <25} {(users[0].balance/100):6.2f}")
    if deposit > 0:
        print(f"{'deposit'.ljust(25)} {(deposit/100):6.2f}")
    if len(products) > 0:
        for product in products:
            print(f"{product.name.ljust(25)} {(-product.price/100):6.2f}")
    print("-"*32)
    print(f"{'new balance'.ljust(25)} {(total/100):6.2f}")

def startScreen(font):
    logo(font)
    print("")
    print(info(f"Score: {font.score}"))
    print(info("Psstt... (u)pvote or (d)ownvote this logo!"))

def randomFont(session):
    return session.query(Font).order_by(func.random()).first()

def main(Session):
    isRunning = True
    with Session() as session:
        font = randomFont(session)
        startScreen(font)
        scanned = input(question("\nType nickname or scan barcode: "))

        users = []

        if scanned.lower() == "q":
            isRunning = False
        elif scanned == "u":
            font.score += 1
            font = None
        elif scanned == "d":
            font.score -= 1
            font = None
        elif scanned == "":
            pass
        else:
            for userQuery in session.query(User).filter(func.lower(User.name)==scanned.lower()):
                users.append(userQuery)
            assert len(users) < 2, "Database returned multiple users!"
            # We could not find this user in our DB
            if len(users) == 0:
                print(f"{scanned} is not registered")
                yn = input_yesno("Do you wish to register this user?")
                if yn == "y":
                    user = User(name=scanned, balance=0)
                    users.append(user)
                    session.add(user)
                    session.commit()

        # We found a user or they have just registered
        if len(users) == 1:
            userBusy = True
            products = []
            deposit = 0

            while userBusy:
                total = users[0].balance + deposit
                for product in products:
                    total -= product.price
                purchaseScreen(users, products, deposit, total, font)
                scanned = input(question("\nType command(A,C,D) or scan product: "))
                if scanned.lower() == "d":
                    deposit += input_deposit()
                elif scanned.lower() == "a":
                    totalPrice = 0
                    for product in products:
                        totalPrice += product.price
                    if totalPrice <= (users[0].balance + deposit):
                        users[0].balance += deposit
                        users[0].balance -= totalPrice
                        print(succes("Transaction confirmed!"))
                        time.sleep(2)
                        # LOG
                        userBusy = False
                    else:
                        print(warning(f"Not enough funds! You need an additional {(total*-0.01):.2f}"))
                        time.sleep(1)
                elif scanned.lower() == "c":
                    print(warning(f"Transaction canceled!"))
                    session.rollback()
                    userBusy = False
                    time.sleep(2)
                else:
                    productQueries = []
                    for productQuery in session.query(Product).filter(Product.barcode==scanned):
                        productQueries.append(productQuery)
                    if len(productQueries) == 0:
                        print(warning("Invalid product code."))
                        time.sleep(1)
                    else:
                        products.extend(productQueries)
        session.commit()
    return isRunning

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    isRunning = True
    font = None
    while isRunning:
        isRunning = main(Session)
