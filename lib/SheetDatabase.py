import gspread
from google.oauth2.service_account import Credentials

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# Add your service account file
creds = Credentials.from_service_account_file('./key_gs.json', scopes=scope)

client = gspread.authorize(creds)


# store and retrieve all data from A1. Input should be a dictionary with the server id as the key
class _SheetDatabase:
    def __init__(self):
        self.sheet = client.open('chirp-bot-prod')
        self.worksheet = self.sheet.get_worksheet(0)

    def get_data(self, key='B2') -> str:
        data = self.worksheet.get(key)
        if len(data) > 0:
            return data[0][0]
        else:
            print('[WARN] no data')
            return None
        

    def set_data(self, value, key='B2'):
        if type(value) == dict:
            print('[ERROR] incorrect data type within set_data')
        self.worksheet.update_cell(2, 2, value)



sheet_database = _SheetDatabase()
