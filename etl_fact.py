import pandas as pd
from connection import source_engine, dwh_engine

COLUMNS = ["TransactionID", "AccountID", "TransactionDate",
           "Amount", "TransactionType", "BranchID"]

def extract_from_db():
    df = pd.read_sql("SELECT * FROM transaction_db", source_engine())
    df.columns = COLUMNS
    print(f"  DB source:    {len(df)} rows")
    return df

def extract_from_excel(filepath="transaction_excel.xlsx"):
    df = pd.read_excel(filepath)
    df.columns = COLUMNS
    print(f"  Excel source: {len(df)} rows")
    return df

def extract_from_csv(filepath="transaction_csv.csv"):
    df = pd.read_csv(filepath)
    df.columns = COLUMNS
    print(f"  CSV source:   {len(df)} rows")
    return df

def load_fact_transaction():
    print("Extracting from all 3 sources...")
    db_df    = extract_from_db()
    excel_df = extract_from_excel()
    csv_df   = extract_from_csv()

    # Merge all 3 sources into one DataFrame
    combined = pd.concat([db_df, excel_df, csv_df], ignore_index=True)
    print(f"\n  Total before dedup: {len(combined)} rows")

    # Deduplicate by TransactionID — keep first occurrence
    combined = combined.drop_duplicates(subset=["TransactionID"], keep="first")
    print(f"  Total after dedup:  {len(combined)} rows")

    # Ensure correct data types
    combined["TransactionDate"] = pd.to_datetime(combined["TransactionDate"])
    combined["Amount"]          = combined["Amount"].astype(int)
    combined["TransactionID"]   = combined["TransactionID"].astype(int)
    combined["AccountID"]       = combined["AccountID"].astype(int)
    combined["BranchID"]        = combined["BranchID"].astype(int)

    combined.to_sql("FactTransaction", dwh_engine(), if_exists="append", index=False)
    print(f"\n✅ FactTransaction loaded: {len(combined)} rows")

if __name__ == "__main__":
    load_fact_transaction()
