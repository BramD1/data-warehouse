from connection import raw_connection

def create_sp_daily_transaction():
    conn = raw_connection("DWH")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('DailyTransaction', 'P') IS NOT NULL
            DROP PROCEDURE DailyTransaction
    """)

    cursor.execute("""
        CREATE PROCEDURE DailyTransaction
            @start_date DATE,
            @end_date   DATE
        AS
        BEGIN
            SELECT
                CAST(TransactionDate AS DATE) AS Date,
                COUNT(*)                      AS TotalTransactions,
                SUM(Amount)                   AS TotalAmount
            FROM FactTransaction
            WHERE CAST(TransactionDate AS DATE) BETWEEN @start_date AND @end_date
            GROUP BY CAST(TransactionDate AS DATE)
            ORDER BY Date
        END
    """)

    conn.close()
    print("✅ Stored Procedure DailyTransaction created")

def create_sp_balance_per_customer():
    conn = raw_connection("DWH")
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        IF OBJECT_ID('BalancePerCustomer', 'P') IS NOT NULL
            DROP PROCEDURE BalancePerCustomer
    """)

    cursor.execute("""
        CREATE PROCEDURE BalancePerCustomer
            @name NVARCHAR(100)
        AS
        BEGIN
            SELECT
                dc.CustomerName,
                da.AccountType,
                da.Balance,
                da.Balance + SUM(
                    CASE
                        WHEN ft.TransactionType = 'Deposit' THEN  ft.Amount
                        ELSE                                      -ft.Amount
                    END
                ) AS CurrentBalance
            FROM DimCustomer     dc
            JOIN DimAccount      da ON dc.CustomerID = da.CustomerID
            JOIN FactTransaction ft ON da.AccountID  = ft.AccountID
            WHERE dc.CustomerName LIKE '%' + UPPER(@name) + '%'
              AND da.Status = 'active'
            GROUP BY dc.CustomerName, da.AccountType, da.Balance
        END
    """)

    conn.close()
    print("✅ Stored Procedure BalancePerCustomer created")

if __name__ == "__main__":
    create_sp_daily_transaction()
    create_sp_balance_per_customer()
