Overview

An ETL pipeline that reads nested JSON data, flattens and cleans it
using Python/Pandas, loads it into SQL Server, and runs business queries.

Tech Stack:
Python 3.10+
Pandas (json_normalize, fillna, apply)
SQL Server / SSMS 22
SQLAlchemy + pyodbc

Pipeline Steps:
Extract - Load raw nested JSON
Transform - Flatten, clean nulls, derive salary_band column
Load - Insert into SQL Server (dbo.employees)
Analyze - Run 4 business queries

Key Skills Demonstrated:
JSON flattening with pd.json_normalize()
Null handling with fillna(mean)
SQL Server connection via SQLAlchemy
Window functions in T-SQL

How to Run:
pip install -r requirements.txt
Create CompanyDB in SSMS
Update SERVER name in pipeline.py
python pipeline.py
Open queries.sql in SSMS and run each query
