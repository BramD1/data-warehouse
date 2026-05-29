from sqlalchemy import create_engine
import pyodbc

PASSWORD = "YourPassword123!"  # same password from docker run
DRIVER   = "ODBC+Driver+18+for+SQL+Server"

def source_engine():
    return create_engine(
        f"mssql+pyodbc://sa:{PASSWORD}@localhost,1433/sample"
        f"?driver={DRIVER}&TrustServerCertificate=yes"
    )

def dwh_engine():
    return create_engine(
        f"mssql+pyodbc://sa:{PASSWORD}@localhost,1433/DWH"
        f"?driver={DRIVER}&TrustServerCertificate=yes"
    )

def raw_connection(database="master"):
    """Raw pyodbc connection for DDL (CREATE DATABASE, stored procedures)"""
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER=localhost,1433;DATABASE={database};"
        f"UID=sa;PWD={PASSWORD};"
        f"TrustServerCertificate=yes;"
    )