import pyodbc
from pyodbc import Connection
import pandas as pd

def connect():
    # Some other example server values are
    # server = 'localhost\sqlexpress' # for a named instance
    # server = 'myserver,port' # to specify an alternate port
    server = 'HIPLI-XASDO' 
    database = 'Boaz' 
    #username = 'myusername' 
    #password = 'mypassword' 
    # ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
    #cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password)
    connection = pyodbc.connect(f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server};DATABASE={database};ENCRYPT=no;Trusted_Connection=yes")
    return connection

def query1(connection: Connection):
    df = pd.read_sql_query('SELECT * FROM AF_Terms', connection)
    print(df)



if __name__ == "__main__":

    connection = connect()
    query1(connection)
    x = 1