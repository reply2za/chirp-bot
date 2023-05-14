import gspread
from google.oauth2.service_account import Credentials

from lib.ProcessManager import process_manager

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# Add your service account file
creds = Credentials.from_service_account_file('./key_gs.json', scopes=scope)

client = gspread.authorize(creds)

PROD_CELL = 'B2'
DEV_CELL = 'B3'
CELL_TO_USE = DEV_CELL if process_manager.is_dev_mode() else PROD_CELL

# store and retrieve all data from A1. Input should be a dictionary with the server id as the key
class _SheetDatabase:
    def __init__(self):
        self.sheet = client.open('chirp-bot-prod')
        self.worksheet = self.sheet.get_worksheet(0)

    def get_data(self, key=CELL_TO_USE) -> str:
        data = self.worksheet.get(key)
        if len(data) > 0:
            return data[0][0]
        else:
            print('[WARN] no data')
            return None
        

    def set_data(self, value, key=CELL_TO_USE):
        if key[0] != 'B':
            raise Exception('key must be a cell in column B')
        
        if type(value) == dict:
            print('[ERROR] incorrect data type within set_data')
        self.worksheet.update_cell(key[1], 2, value)



sheet_database = _SheetDatabase()
