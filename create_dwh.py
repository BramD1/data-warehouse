import pyodbc
from connection import raw_connection

def create_database():
    conn = raw_connection("master")
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'DWH')
        CREATE DATABASE DWH
    """)
    conn.close()
    print(" Database DWH created (or already exists)")

def create_tables():
    conn = raw_connection("DWH")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('FactTransaction', 'U') IS NOT NULL DROP TABLE FactTransaction;
        IF OBJECT_ID('DimAccount', 'U')      IS NOT NULL DROP TABLE DimAccount;
        IF OBJECT_ID('DimCustomer', 'U')     IS NOT NULL DROP TABLE DimCustomer;
        IF OBJECT_ID('DimBranch', 'U')       IS NOT NULL DROP TABLE DimBranch;
    """)

    cursor.execute("""
        CREATE TABLE DimCustomer (
            CustomerID   INT          PRIMARY KEY,
            CustomerName NVARCHAR(100),
            Address      NVARCHAR(200),
            CityName     NVARCHAR(100),
            StateName    NVARCHAR(100),
            Age          INT,
            Gender       NVARCHAR(20),
            Email        NVARCHAR(100)
        )
    """)

    cursor.execute("""
        CREATE TABLE DimAccount (
            AccountID   INT          PRIMARY KEY,
            CustomerID  INT          FOREIGN KEY REFERENCES DimCustomer(CustomerID),
            AccountType NVARCHAR(50),
            Balance     BIGINT,
            DateOpened  DATE,
            Status      NVARCHAR(20)
        )
    """)

    cursor.execute("""
        CREATE TABLE DimBranch (
            BranchID       INT          PRIMARY KEY,
            BranchName     NVARCHAR(100),
            BranchLocation NVARCHAR(200)
        )
    """)

    cursor.execute("""
        CREATE TABLE FactTransaction (
            TransactionID   INT          PRIMARY KEY,
            AccountID       INT          FOREIGN KEY REFERENCES DimAccount(AccountID),
            BranchID        INT          FOREIGN KEY REFERENCES DimBranch(BranchID),
            TransactionDate DATETIME,
            Amount          BIGINT,
            TransactionType NVARCHAR(50)
        )
    """)

    conn.close()
    print(" All DWH tables created with PKs and FKs")

if __name__ == "__main__":
    create_database()
    create_tables()