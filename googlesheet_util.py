import gspread
from google.oauth2.service_account import Credentials
import os

# Initiate google sheet api
scopes = [
    "https://www.googleapis.com/auth/spreadsheets"
]

current_dir = os.path.dirname(os.path.abspath(__file__))
creds_path = os.path.join(current_dir, "credentials.json")

creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
client = gspread.authorize(creds)

sheet_id = ["1Atdn51YA1fwYOJGK6tieY939RFUZDqh1uTnb9EbG_G4",  # 日場門票 # TODO: 檢查google sheet鏈接
            "1DjjarTf4Bd8fBkzaWRTxvM71uU2tohJm2W5SOM34t4E",  # 套票
            "1rM8Oc8xrvqvNQ1OxshxUnx_xEQwe5OUZlSLGFjC6YR4"]  # 城大師生


def getData() -> list[list[list]]:
    data = []
    for i in range(3):
        sheet = client.open_by_key(sheet_id[i])
        sheet_data = sheet.sheet1.get_all_values()
        data.append([[i] + row for row in sheet_data if row[0] != ""])  # 添加sheet id，從0開始數，移除空record
        data[-1] = [[j + 1] + row for j, row in enumerate(data[-1])]  # 添加record id，從1開始數
    # for i in data:
    #     print(len(i))
    #     for j in i:
    #         print(j)
    return data  # [record_id, sheet_id, ...]


def updateStatus(sheet_number, record_id, col):
    sheet = client.open_by_key(sheet_id[sheet_number])
    sheet.sheet1.update_cell(record_id, col, "已發送") #col和row都是從1開始數
