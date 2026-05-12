import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define your scope and credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("your_credentials.json", scope)
client = gspread.authorize(creds)

# Open your Google Sheet by name or URL
sheet = client.open("My Sheet").sheet1  # Or use .worksheet("Sheet2")

# Load your local data (can be CSV, Excel, DB, etc.)
df = pd.read_csv("daily_data.csv")  # or generate your DataFrame

# Clear the sheet first if needed
sheet.clear()

# Update sheet with new data
sheet.update([df.columns.values.tolist()] + df.values.tolist())
