from create_dwh        import create_database, create_tables
from etl_dimensions    import load_dim_customer, load_dim_account, load_dim_branch
from etl_fact          import load_fact_transaction
from stored_procedures import create_sp_daily_transaction, create_sp_balance_per_customer

if __name__ == "__main__":
    print("\n" + "="*45)
    print("   STEP 1: Create DWH Database & Tables")
    print("="*45)
    create_database()
    create_tables()

    print("\n" + "="*45)
    print("   STEP 2: Load Dimension Tables")
    print("="*45)
    load_dim_customer()   # First — DimAccount has FK to DimCustomer
    load_dim_account()
    load_dim_branch()

    print("\n" + "="*45)
    print("   STEP 3: Load Fact Table")
    print("="*45)
    load_fact_transaction()

    print("\n" + "="*45)
    print("   STEP 4: Create Stored Procedures")
    print("="*45)
    create_sp_daily_transaction()
    create_sp_balance_per_customer()

    print("\n" + "="*45)
    print("   ✅ Pipeline Complete!")
    print("="*45)
