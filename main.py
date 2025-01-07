import logging
import os
from datetime import datetime
import requests
import googlesheet_util as gsutil
import email_util as eutil
from ticket_code_util import gen_code

if not os.path.exists("log"):  # 生成log目錄
    os.mkdir("log")

# 獲取當前時間並格式化為字符串
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
# 設置logging配置
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
logging.basicConfig(level=logging.DEBUG, filename=f"log\\{current_time}.log", filemode='w', format=FORMAT,
                    encoding='utf-8')
logging.getLogger().setLevel(logging.DEBUG)
# 創建一個控制台處理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter(FORMAT))

# 獲取根日誌記錄器並添加控制台處理器
logger = logging.getLogger()
logger.addHandler(console_handler)


data = gsutil.getData()
sending_list = []

# 記錄每張sheet的column位置
email_send_column = []  # 買家的email
value_column = []
paid_column = []
email_verify_column = []  # 確認email已經發送

for sheet in data:
    try:
        email_send_column.append(sheet[0].index("Email Address"))
        value_column.append(sheet[0].index("門票數量"))
        paid_column.append(sheet[0].index("checked已付款"))
        email_verify_column.append(sheet[0].index("email已發送"))
    except ValueError:
        logging.error("無法找到欄位，請檢查google sheet")
        exit(0)

for sheet_id in range(len(data)):
    for record in data[sheet_id]:
        if record[paid_column[sheet_id]] == "TRUE" and record[email_verify_column[sheet_id]] != "已發送":
            sending_list.append(record)

# 按時間排序
sorted_sending_list = sorted(sending_list, key=lambda x: datetime.strptime(x[2], "%m/%d/%Y %H:%M:%S"))

for record in sorted_sending_list:
    email = record[email_send_column[record[1]]]
    value = int(record[value_column[record[1]]])

    # gen ticket code
    codeList = gen_code(value)

    # 更新ticket db
    id = []
    for code in codeList:
        rsp = requests.get(f"http://localhost:8080/ticket/create/{code}/{email}")
        if rsp.status_code == 200:
            id.append(int(rsp.text))

    # 發送email
    eutil.send_email(codeList, id, email)

    # 更新status
    gsutil.updateStatus(record[1], record[0], email_verify_column[record[1]] - 1)
