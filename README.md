# ACKbar
Buying drinks and snacks in your hacker-/maker-/foospace is easy with ACKbar.

Don't burden your participants with calculating change; math is for nerds.
Instead, create an account and enjoy the benefits of having an account balance.

Accounts don't have passwords because it didn't make sense for our usecase.

## Run
Run with 'python app.py'

## Requirements
python 3.6+
sqlalchemy
pymysql

## config
Change username and password in credentials.txt file.
Uncomment one of two SQLALCHEMY_DATABASE_URI lines in 'database.py' to use either mariadb or sqlite.
