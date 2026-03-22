import json  # Import built-in module to work with JSON files
import pandas as pd  # Import pandas library for data manipulation (not yet used here)

import pyodbc
from sqlalchemy import create_engine, text

# === STEP 1: EXTRACT ===
with open("data/employees.json", "r") as f:  # Open the JSON file in read mode
    raw_data = json.load(f)  # Load the contents of the file into a Python dictionary

# Preview the raw data
print("Raw JSON loaded successfully.")  # Confirm that the file was loaded
print(f"Number of employees: {len(raw_data['employees'])}")  # Print total number of employee records
print(raw_data["employees"][0])  # Print the first employee record to inspect the structure

# === STEP 2: TRANSFORM ===

# Flatten nested JSON (address.city, address.country become columns)
df = pd.json_normalize(raw_data['employees'])  # Convert the list of employee dictionaries into a flat table (DataFrame), expanding nested fields like address into separate columns

print("\nColumns after flattening:")  # Print a heading to indicate we're showing the column names after transformation
print(df.columns.tolist())  # Display all column names in the DataFrame as a list

# --- Clean column names (replace dots with underscores) ---
df.columns = df.columns.str.replace('.', '_', regex=False)  # Replace '.' in column names (e.g., address.city) with '_' to make them easier to work with

# --- Standardise text fields to lowercase ---
df['department'] = df['department'].str.lower()  # Convert all department names to lowercase for consistency
df['name'] = df['name'].str.title()  # Convert names to title case (e.g., john -> John)

# --- Handle missing salary: fill with mean ---
mean_salary = df['salary'].mean()  # Calculate the average salary (ignoring missing values)
df['salary'] = df['salary'].fillna(mean_salary).round(2)  # Fill missing salary values with the mean and round to 2 decimal places

# --- Add a derived column: salary band ---
def salary_band(sal):  # Define a function to categorize salary into bands
    if sal < 4800: return 'Low'  # If salary is less than 4800, label as 'Low'
    elif sal <= 5500: return 'Mid'  # If salary is between 4800 and 5500, label as 'Mid'
    else: return 'High'  # If salary is above 5500, label as 'High'

df['salary_band'] = df['salary'].apply(salary_band)  # Apply the function to each salary value to create a new column

print("\nCleaned DataFrame:")  # Print a heading to indicate cleaned data
print(df)  # Display the final cleaned and transformed DataFrame

# === STEP 3: LOAD ===

# --- Connection string (update SERVER_NAME to your instance) ---
SERVER   = 'localhost\\SQLEXPRESS'          # SQL Server instance name (e.g., localhost or localhost\\SQLEXPRESS)
DATABASE = 'CompanyDB'          # Target database name in SQL Server

# Build the connection string using SQLAlchemy format
conn_str = (
    f'mssql+pyodbc://{SERVER}/{DATABASE}'   # Specifies SQL Server + pyodbc driver
    '?driver=ODBC+Driver+17+for+SQL+Server' # ODBC driver used to connect to SQL Server
    '&trusted_connection=yes'               # Uses Windows Authentication (no username/password)
)

# Create a SQLAlchemy engine (this manages the DB connection)
engine = create_engine(conn_str)

# --- Write DataFrame to SQL Server ---
with engine.connect() as conn:   # Open a connection to the database
    df.to_sql(
        name='employees',        # Name of the table to create/write into
        con=conn,                # Database connection object
        schema='dbo',            # Schema where table will be created (default is dbo)
        if_exists='replace',     # If table exists, DROP it and recreate it
        index=False              # Do NOT write DataFrame index as a column
    )
    conn.commit()               # Commit the transaction to save changes

# Print success message
print("\nData loaded into SQL Server successfully!")

# Print number of rows inserted (length of DataFrame)
print(f"Rows inserted: {len(df)}")