from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import mysql.connector

app = FastAPI()

# MySQL database configuration
db_config = {
    "host": "localhost",
    "database": "eia_cc",
    "user": "your_mysql_username",
    "password": "your_mysql_password",
}

# Function to insert distinct values into a MySQL table
def insert_distinct_values(table_name, distinct_values):
    try:
        conn = mysql.connector.connect(host='localhost', database='eia_cc', user='root')
        cursor = conn.cursor()
        print("Database connection successful")

        # Iterate through distinct values and insert only if they don't already exist
        for value in distinct_values:
            query = f"INSERT INTO {table_name} ({table_name}) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE {table_name} = %s)"
            cursor.execute(query, (value, value))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        return False

@app.post("/upload")
async def upload_excel_file():
    try:
        # Read the Excel file into a pandas DataFrame
        data = pd.read_excel('app\eia_cc\excel_test.xlsx')

        # Define a dictionary to store the "town" column data with districts as keys
        town_data = {}

        # Iterate through the rows to separate "town" data with different districts
        for _, row in data.iterrows():
            town = row["towns_tbl"]
            district = row["districts_tbl"]

            # Check if the town is already in the dictionary
            if town in town_data:
                # If the district is the same, consider it a duplicate and skip
                if town_data[town] == district:
                    continue
                else:
                    # If the district is different, append the district to the town name
                    town = f"{town} ({district})"

            town_data[town] = district

        # Iterate through the "town" data with districts and insert into MySQL table
        distinct_town_data = list(town_data.keys())
        if insert_distinct_values("towns_tbl", distinct_town_data):
            print("Distinct town values inserted into towns_tbl successfully.")
        else:
            print("Failed to insert distinct town values into towns_tbl.")

        # Iterate through the other columns and insert distinct values into corresponding MySQL tables
        for column_name in data.columns:
            if column_name != "town":
                distinct_values = data[column_name].unique().tolist()
                if insert_distinct_values(f"{column_name}", distinct_values):
                    print(f"Distinct values inserted into {column_name} successfully.")
                else:
                    print(f"Failed to insert distinct values into {column_name}.")

        return JSONResponse(content={"message": "Distinct values inserted into MySQL tables successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})