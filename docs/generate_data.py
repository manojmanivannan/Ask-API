import pandas as pd
from faker import Faker
import random
import os

# Initialize Faker
fake = Faker()

# Generate synthetic crime records data
crime_records = []

for _ in range(1000):  # Generating 1000 mock crime records
    crime_record = {
        'Crime Record ID': fake.uuid4(),
        'Date': fake.date_this_year(),
        'Time': fake.time(),
        'Location': fake.address().replace('\n', ', '),
        'Type of Crime': random.choice(['Robbery', 'Assault', 'Burglary', 'Homicide', 'Fraud']),
        'Suspects': fake.name(),
        'Victims': fake.name(),
        'Witnesses': fake.name(),
        'Description': fake.text().replace('\n', ', ')
    }
    crime_records.append(crime_record)

# Create a DataFrame
crime_records_df = pd.DataFrame(crime_records)

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))


# Save the DataFrame to a CSV file in the same directory as the script
csv_file_path = os.path.join(current_directory, 'mock_crime_records.csv')
crime_records_df.to_csv(csv_file_path, index=False)