![Data Warehouse ETL Pipeline](https://media.geeksforgeeks.org/wp-content/uploads/20250127161828904427/data_warehouse-660.webp)

> source img: https://www.geeksforgeeks.org/big-data/data-warehousing/

# Project Title: Data Warehouse

## 📝 Overview
As a Data Engineer Intern at ID/X Partners (via Rakamin Academy), my job is to build a Data Warehouse and ETL pipeline for a banking client. The client had data scattered across multiple sources (Excel, CSV, and SQL Server) and struggled to consolidate them for reporting and analysis. The goal was to centralise everything into a single Data Warehouse with clean, deduplicated data and stored procedures for quick reporting.

## 🔧 Technologies Used
**Programming Language:** Python

**Libraries:** Pandas, pyodbc, SQLAlchemy, openpyxl

**Tools:** SQL Server Management Studio (SSMS), Docker, SQL Server 2022

## 🚀 Workflow

### 1️⃣ Prerequisites & Setup
Before running the pipeline, the following must be ready:
1. Docker Desktop running with SQL Server 2022 container started (`docker start sqlserver`)
2. Source database restored from `sample.bak` via SSMS
3. Python environment with required libraries installed (`pip install pandas pyodbc sqlalchemy openpyxl`)
4. `transaction_excel.xlsx` and `transaction_csv.csv` placed in the project folder

### 2️⃣ Source Data
The banking client had data stored across 8 different sources:
1. `transaction_excel.xlsx` — transaction records in Excel format
2. `transaction_csv.csv` — transaction records in CSV format
3. `transaction_db` — transaction records in SQL Server
4. `account` — bank account data (SQL Server)
5. `customer` — customer profile data (SQL Server)
6. `branch` — branch office data (SQL Server)
7. `city` — city/district reference data (SQL Server)
8. `state` — province/state reference data (SQL Server)

### 3️⃣ Data Warehouse Design
Created a new database `DWH` with a star schema consisting of:
- **DimCustomer** — built from joining `customer`, `city`, and `state` tables. Text columns (CustomerName, Address, CityName, StateName, Gender) are stored in UPPERCASE. Columns follow PascalCase naming.
- **DimAccount** — account data with FK to DimCustomer
- **DimBranch** — branch office data
- **FactTransaction** — central fact table with FK to DimAccount and DimBranch

### 4️⃣ ETL Pipeline
The pipeline is split into modular Python scripts:

1. **`connection.py`** — Database connection setup for both source and DWH using SQLAlchemy and pyodbc
2. **`create_dwh.py`** — Creates the DWH database and all 4 tables with primary keys and foreign key constraints
3. **`etl_dimensions.py`** — Extracts and loads all 3 dimension tables from the source database
4. **`etl_fact.py`** — Merges transactions from all 3 sources (Excel, CSV, DB), deduplicates by `TransactionID`, and loads into `FactTransaction`
5. **`stored_procedures.py`** — Creates 2 stored procedures in the DWH
6. **`pipeline.py`** — Orchestrates all steps in the correct dependency order

To run the full pipeline:
```bash
python pipeline.py
```

### 5️⃣ Stored Procedures
Two stored procedures were created for quick business reporting:

- **`DailyTransaction`** — accepts `@start_date` and `@end_date` parameters, returns daily transaction count and total amount within the date range

```sql
EXEC DailyTransaction @start_date='2024-01-18', @end_date='2024-01-20'
```

- **`BalancePerCustomer`** — accepts `@name` parameter, returns CustomerName, AccountType, Balance, and computed CurrentBalance (Deposit adds to balance, Transfer/Withdrawal subtracts). Filters active accounts only.

```sql
EXEC BalancePerCustomer @name='Shelly'
```

### 6️⃣ Conclusion & Suggestions
The ETL pipeline successfully consolidates data from 3 different source formats into a single, clean Data Warehouse. Duplicate transactions across sources are handled automatically, and the stored procedures allow the client to get reporting results instantly without manual data extraction.

Potential improvements for the future:
- Add logging to track each pipeline run and row counts
- Add error handling and rollback if any step fails midway
- Schedule the pipeline to run automatically using Apache Airflow
- Add data validation checks before loading (e.g. null checks, type checks)

## Thank You For Visiting!!

📬 Connect with me and give me feedback

💼 LinkedIn: https://www.linkedin.com/in/bramantyo-anandaru-suyadi-0b9729208/