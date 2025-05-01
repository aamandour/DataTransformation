import pandas as pd

# Load the larger dataset
df = pd.read_csv('bc_veh4223_230215.csv')

# Step 1: Decode TIMESTAMP from OPD_DATE + ACT_TIME
df['OPD_DATE'] = pd.to_datetime(df['OPD_DATE'], format='%d%b%Y:%H:%M:%S')

def create_timestamp(row):
    return pd.Timestamp(row['OPD_DATE']) + pd.Timedelta(seconds=row['ACT_TIME'])

df['TIMESTAMP'] = df.apply(create_timestamp, axis=1)

# Drop OPD_DATE and ACT_TIME as they're now merged into TIMESTAMP
df = df.drop(columns=['OPD_DATE', 'ACT_TIME'])

# Step 2: Compute SPEED per trip using groupby
df['dMETERS'] = df.groupby('EVENT_NO_TRIP')['METERS'].diff()
df['dTIME'] = df.groupby('EVENT_NO_TRIP')['TIMESTAMP'].diff().dt.total_seconds()

# Compute SPEED, set to 0.0 if dTIME is missing or non-positive
df['SPEED'] = df.apply(
    lambda row: row['dMETERS'] / row['dTIME'] if pd.notnull(row['dTIME']) and row['dTIME'] > 0 else 0.0,
    axis=1
)

# Drop intermediate delta columns
df = df.drop(columns=['dMETERS', 'dTIME'])

# Step 3: Filter for vehicle #4223 only
vehicle_df = df[df['VEHICLE_ID'] == 4223]

# Step 4: Analyze valid SPEED values
valid_speeds = vehicle_df['SPEED'].dropna()
max_speed = valid_speeds.max()
median_speed = valid_speeds.median()

# Get the row where max speed occurred
max_row = vehicle_df[vehicle_df['SPEED'] == max_speed].iloc[0]

# Step 5: Display results
print("\n--- Speed Analysis for Vehicle #4223 on Feb 15, 2023 ---")
print(f"Maximum Speed: {max_speed:.2f} m/s")
print(f"Occurred at: {max_row['TIMESTAMP']}")
print(f"Location: ({max_row['GPS_LATITUDE']}, {max_row['GPS_LONGITUDE']})")
print(f"Median Speed: {median_speed:.2f} m/s")

# Step 6: Show sample of data
# print("\n--- Sample Data ---")
# print(vehicle_df[['EVENT_NO_TRIP', 'METERS', 'TIMESTAMP', 'SPEED']].head())
# print(vehicle_df.info())
