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
@app.post("/update")
async def update_database():
    try:
        # Read the Excel file into a pandas DataFrame
        data = pd.read_excel('app\eia_cc\excel_test.xlsx')

        # Connect to the MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Iterate through each row in the Excel data
        for index, row in data.iterrows():
            town = row['towns_tbl']  # Assuming 'towns' is the column name in Excel
            region = row['regions_tbl']  # Assuming 'region' is the column name in Excel
            district = row['districts_tbl'] 
            onset = row['rain_onset_tbl']
            zone = row['eco_zone_tbl'] 

            # Find the region_id based on the region name
            query_region_id = "SELECT zone_id FROM eco_zone_tbl WHERE zone = %s"
            cursor.execute(query_region_id, (zone,))
            region_id = cursor.fetchone()

            if region_id:
                region_id = region_id[0]

                # Update the towns_tbl with the found region_id
                query_update_town = "UPDATE regions_tbl SET zone_id = %s WHERE region = %s"
                cursor.execute(query_update_town, (region_id, region))
                conn.commit()
                print(f"Updated region_id for town: {town} with onset_id: {region_id}")
            else:
                print(f"Region not found for town: {town}")

        # Close the database connection
        conn.close()

        return JSONResponse(content={"message": "Updated district_id in towns_tbl successfully"})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})