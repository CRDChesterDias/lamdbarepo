import pandas as pd
from sqlalchemy import create_engine

# --- Database connection details ---
db_type = 'postgresql'  # Change to 'mysql', 'mssql+pyodbc', etc.
username = 'your_username'
password = 'your_password'
host = 'your_host'        # e.g., 'localhost' or IP
port = '5432'             # Change as per DB type
database = 'your_database'

# Create database connection string
connection_string = f"{db_type}://{username}:{password}@{host}:{port}/{database}"
engine = create_engine(connection_string)

# --- SQL query ---
query = """
SELECT *
FROM your_table
WHERE some_column = 'some_value';
"""

# --- Execute query and save to CSV ---
try:
    # Run query
    df = pd.read_sql(query, engine)
    
    # Write to CSV
    df.to_csv('output.csv', index=False)
    print("Query executed successfully. Output saved to 'output.csv'.")

except Exception as e:
    print(f"Error: {e}")

finally:
    # Close connection
    engine.dispose()
