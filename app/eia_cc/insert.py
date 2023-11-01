from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import pandas as pd
import mysql.connector

app = FastAPI()

# MySQL database configuration
db_config = {
    "host": "localhost",
    "database": "eia_cc",
    "user": "root",
    "password": "",
}

# Function to insert distinct values into a MySQL table
# table_name, distinct_values
def insert_distinct_values(table_name, distinct_values):
    try:
        conn = mysql.connector.connect(host='localhost', database='eia_cc', user='root')
        cursor = conn.cursor()
        print("Database connection successful")

         # Iterate through distinct values and insert only if they don't already exist
        for value in distinct_values:
            query = f"INSERT INTO {table_name} ({table_name}) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE {table_name} = %s)"
            print(query)
            cursor.execute(query, (value, value))

        # # Prepare and execute the SQL query to insert distinct values
        # query = f"INSERT INTO {table_name} ({table_name}) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE {table_name} = %s)"
        # f"INSERT INTO {table_name} ({table_name}) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM {table_name} WHERE {table_name} = %s)"
        
        # print(query)
        # cursor.executemany(query, [(value,) for value in distinct_values])
        # cursor.execute(query, (value, value))

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        return {"message": "successs"}
    except Exception as e:
        return False

@app.post("/upload")
def upload_excel_file():
    try:
        # print('kyeiwaa')
        # Read the Excel file into a pandas DataFrame
        data = pd.read_excel('app\eia_cc\excel_test.xlsx')
        # print (len(data))
        # insert_distinct_values()
        # print(data)

        # Iterate through the columns and insert distinct values into corresponding MySQL tables
        for column_name in data.columns:
            distinct_values = data[column_name].unique().tolist()
            # print(f"{column_name}", distinct_values)
            # insert_distinct_values(f"{column_name}", distinct_values)
            if insert_distinct_values(f"{column_name}", distinct_values):
                print(f"Distinct values inserted into {column_name} successfully.")
            else:
                print(f"Failed to insert distinct values into {column_name}.")

        return JSONResponse(content={"message": "Distinct values inserted into MySQL tables successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})