import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('bc_trip259172515_230215.csv')

# Drop the EVENT_NO_STOP column
df = df.drop(columns=['EVENT_NO_STOP'])

# Display the columns after dropping EVENT_NO_STOP column
print(df.columns)

# Drop GPS_SATELLITES and GPS_HDOP columns
df = df.drop(columns=['GPS_SATELLITES', 'GPS_HDOP'])

# Display the columns after dropping GPS_SATELLITES and GPS_HDOP columns
print(df.columns)













# Show basic info about the dataset
print(df.info())

# Print how many breadcrumb records there are
print(f"Total number of breadcrumb records: {len(df)}")
