import pandas as pd
from connection import source_engine, dwh_engine

def load_dim_customer():
    src = source_engine()

    # Join customer + city + state to get CityName and StateName
    query = """
        SELECT
            c.customer_id,
            c.customer_name,
            c.address,
            ci.city_name,
            s.state_name,
            c.age,
            c.gender,
            c.email
        FROM customer c
        JOIN city  ci ON c.city_id    = ci.city_id
        JOIN state s  ON ci.state_id  = s.state_id
    """
    df = pd.read_sql(query, src)

    # Rename to PascalCase
    df.columns = ["CustomerID", "CustomerName", "Address",
                  "CityName", "StateName", "Age", "Gender", "Email"]

    # UPPERCASE all text columns EXCEPT CustomerID, Age, Email
    for col in ["CustomerName", "Address", "CityName", "StateName", "Gender"]:
        df[col] = df[col].str.upper()

    df.to_sql("DimCustomer", dwh_engine(), if_exists="append", index=False)
    print(f" DimCustomer loaded: {len(df)} rows")

def load_dim_account():
    src = source_engine()
    df = pd.read_sql("SELECT * FROM account", src)

    df.columns = ["AccountID", "CustomerID", "AccountType",
                  "Balance", "DateOpened", "Status"]

    df.to_sql("DimAccount", dwh_engine(), if_exists="append", index=False)
    print(f" DimAccount loaded: {len(df)} rows")

def load_dim_branch():
    src = source_engine()
    df = pd.read_sql("SELECT * FROM branch", src)

    df.columns = ["BranchID", "BranchName", "BranchLocation"]

    df.to_sql("DimBranch", dwh_engine(), if_exists="append", index=False)
    print(f" DimBranch loaded: {len(df)} rows")

if __name__ == "__main__":
    # Order matters: DimCustomer first (DimAccount has FK to it)
    load_dim_customer()
    load_dim_account()
    load_dim_branch()