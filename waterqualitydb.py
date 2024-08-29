import pyodbc
import pandas as pd

# Define DSN and connection parameters
dsn = 'waterqualitydb'

# Connect to the database
try:
    connection = pyodbc.connect(f'DSN={dsn}')
    print("Database connection successful.")
except pyodbc.Error as e:
    print(f"Database connection error: {e}")
    exit()

# Define queries
queries = {
    'WaterSources': 'SELECT * FROM WaterSources',
    'SamplingLocations': 'SELECT * FROM SamplingLocations',
    'WaterQualityTests': 'SELECT * FROM WaterQualityTests',
    'Contaminants': 'SELECT * FROM Contaminants',
    'TestResults': 'SELECT * FROM TestResults'
}

# Dictionary to store dataframes
dfs = {}

# Execute queries and store results in dataframes
for table_name, query in queries.items():
    try:
        dfs[table_name] = pd.read_sql(query, connection)
    except pd.io.sql.DatabaseError as e:
        print(f"Error reading table {table_name}: {e}")

# Save data to Excel
output_path = 'C:/Users/mtsha/WaterSources.xlsx'
try:
    with pd.ExcelWriter(output_path) as writer:
        for table_name, df in dfs.items():
            df.to_excel(writer, sheet_name=table_name, index=False)
    print(f"Data successfully saved to {output_path}")
except Exception as e:
    print(f"Error saving data to Excel: {e}")

# Close the connection
try:
    connection.close()
    print("Database connection closed.")
except NameError:
    print("Connection was not established.")
