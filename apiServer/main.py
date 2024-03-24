from fastapi import FastAPI, Query, HTTPException
import pandas as pd
import os

app = FastAPI()

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_directory, 'mock_crime_records.csv')

# Load mock crime records CSV
crime_records_df = pd.read_csv(csv_file_path)
crime_records_df['DateTime'] = pd.to_datetime(crime_records_df['Date'] + ' ' + crime_records_df['Time'])

# Drop the original 'Date' and 'Time' columns
crime_records_df.drop(columns=['Date', 'Time'], inplace=True)

@app.get("/search_crime_records/")
async def search_crime_records(location: str = None, date: str = None, crime_type: str = None):
    filtered_records = crime_records_df

    if location:
        filtered_records = filtered_records[filtered_records['Location'].str.contains(location, case=False)]
    
    if date:
        filtered_records = filtered_records[filtered_records['Date'] == date]
    
    if crime_type:
        filtered_records = filtered_records[filtered_records['Type of Crime'] == crime_type]

    if filtered_records.empty:
        raise HTTPException(status_code=404, detail="No records found matching the search criteria")
    
    return filtered_records.to_dict(orient='records')

@app.get("/crime_record_details/")
async def crime_record_details(record_id: str):
    record_details = crime_records_df[crime_records_df['Crime Record ID']==record_id]

    if record_details.empty:
        raise HTTPException(status_code=404, detail="Crime record not found")

    return record_details.to_dict(orient='records')

@app.get("/crime_statistics/")
async def crime_statistics():
    # Implement logic to calculate statistics based on provided parameters
    # This is just a placeholder
    newest = crime_records_df['DateTime'].max().strftime('%Y-%m-%d')
    oldest = crime_records_df['DateTime'].min().strftime('%Y-%m-%d')
    value_counts_of_crime_type = crime_records_df['Type of Crime'].value_counts().to_dict()
    unique_victims = crime_records_df['Victims'].unique().__len__()
    unique_suspects = crime_records_df['Suspects'].unique().__len__()
    unique_witnesses = crime_records_df['Witnesses'].unique().__len__()
    return {
        "oldest_record_date": oldest,
        "newest_record_date": newest,
        "value_counts_of_crime_type": value_counts_of_crime_type,
        "unique_victims": unique_victims,
        "unique_suspects": unique_suspects,
        "unique_witnesses": unique_witnesses
    }

@app.get("/suspects/{record_id}")
async def suspects(record_id: str):
    record_suspects = crime_records_df.loc[crime_records_df['Crime Record ID'] == record_id, 'Suspects'].tolist()

    if not record_suspects:
        raise HTTPException(status_code=404, detail="No suspects found for the given crime record")

    return {"suspects": record_suspects}

@app.get("/victims/{record_id}")
async def victims(record_id: str):
    record_victims = crime_records_df.loc[crime_records_df['Crime Record ID'] == record_id, 'Victims'].tolist()

    if not record_victims:
        raise HTTPException(status_code=404, detail="No victims found for the given crime record")

    return {"victims": record_victims}

@app.get("/witnesses/{record_id}")
async def witnesses(record_id: str):
    record_witnesses = crime_records_df.loc[crime_records_df['Crime Record ID'] == record_id, 'Witnesses'].tolist()

    if not record_witnesses:
        raise HTTPException(status_code=404, detail="No witnesses found for the given crime record")

    return {"witnesses": record_witnesses}
