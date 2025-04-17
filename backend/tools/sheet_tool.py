from pydantic import BaseModel
from googleapiclient.discovery import build
import pickle

# Google Sheet ID
SHEET_ID = "1slKRWH612u43PZ5pJo99sVW7dxDSE01Y6jLl3KwsY9E"  # Replace with your Google Sheet ID

# Predefined Sheet Tabs
SHEET_TABS = {
    "Invoice": "InvoiceSheet!A1",  # Adjust range if needed
    "Visiting Card": "VisitingCardSheet!A1"
}

# === Input Schema for Appending Rows ===
class AppendRowInput(BaseModel):
    sheet_type: str  # One of: Invoice, Visiting Card
    values: list[str]  # A flat row like ["Name", "Email", "Phone"]

# === Append Row Function ===
def append_row_to_sheet(input: AppendRowInput) -> str:
    range_ = SHEET_TABS.get(input.sheet_type)
    if not range_:
        return f"❌ Invalid sheet_type: {input.sheet_type}"

    creds = pickle.load(open("token.pickle", "rb"))
    service = build("sheets", "v4", credentials=creds)

    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=range_,
        valueInputOption="USER_ENTERED",
        body={"values": [input.values]}
    ).execute()

    return f"✅ Row added to {input.sheet_type} sheet."

# === Input Schema for Querying Rows ===
class QuerySheetInput(BaseModel):
    sheet_type: str  # One of: Invoice, Visiting Card
    company_name: str  # The company you want to search for

# === Query Function ===
def query_sheet(input: QuerySheetInput) -> str:
    range_ = SHEET_TABS.get(input.sheet_type)
    if not range_:
        return f"❌ Invalid sheet_type: {input.sheet_type}"

    creds = pickle.load(open("token.pickle", "rb"))
    service = build("sheets", "v4", credentials=creds)

    result = service.spreadsheets().values().get(
        spreadsheetId=SHEET_ID,
        range=range_
    ).execute()

    rows = result.get('values', [])
    if not rows:
        return "❌ No data found in the sheet."

    # Assuming the first row has the headers like ["Name", "Company", "Phone"]
    header = rows[0]
    name_idx = header.index("Name")
    company_idx = header.index("Company")
    phone_idx = header.index("Phone")

    # Filter rows by company name
    found = []
    for row in rows[1:]:  # Skip header row
        if len(row) > company_idx and row[company_idx] == input.company_name:
            name = row[name_idx] if len(row) > name_idx else "Unknown"
            phone = row[phone_idx] if len(row) > phone_idx else "Unknown"
            found.append(f"Name: {name}, Phone: {phone}")

    if not found:
        return f"❌ No contacts found from company {input.company_name}."

    return "\n".join(found)

# === Tool Registration ===
sheets_tool_append = {
    "name": "append_row_to_sheet",
    "description": "Appends a row to either the Invoice or Visiting Card sheet in Google Sheets.",
    "parameters": AppendRowInput.schema(),
    "function": append_row_to_sheet
}

sheets_tool_query = {
    "name": "query_google_sheet",
    "description": "Query the Invoice or Visiting Card sheet for a specific company and return names & numbers.",
    "parameters": QuerySheetInput.schema(),
    "function": query_sheet
}
