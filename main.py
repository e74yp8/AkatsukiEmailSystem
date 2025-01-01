import random
import string
from datetime import datetime
import requests
import googlesheet_util as gsutil
import email_util as eutil

# 3個google sheet
# get曬需要發嘅record -》list
# 按時間排序
# 一個一個發email
# 更新狀態

data = gsutil.getData()
sending_list = []

for sheet in data:
    try:
        paid_column = sheet[0].index("checked已付款")
        email_column = sheet[0].index("email已發送")
    except ValueError:
        print("無法找到欄位，請檢查google sheet")
        exit(0)

    for record in sheet:
        if record[paid_column] == "TRUE" and record[email_column] != "已發送":
            sending_list.append(record)

# 按時間排序
sorted_sending_list = sorted(sending_list, key=lambda x: datetime.strptime(x[2], "%m/%d/%Y %H:%M:%S"))

for record in sorted_sending_list:
    print(record)

    email = record[3]
    value = int(record[5])

    # gen qrcode
    codeSet = set()
    while len(codeSet) < value:
        while True:
            code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))  # 生成128位隨機字元
            try:
                rsp = requests.get("http://localhost:8080/ticket/check_exist/" + code)  # 檢查是否已存在
            except requests.exceptions.RequestException as e:
                raise SystemExit(e)
            if rsp.status_code == 200:
                break
        codeSet.add(code)
    codeList = list(codeSet)

    # 更新ticket db
    id = []
    for code in codeList:
        rsp = requests.get(f"http://localhost:8080/ticket/create/{code}/{email}")
        if rsp.status_code == 200:
            id.append(int(rsp.text))

    # 發送email
    eutil.send_email(codeList, id, "time", email)  # TODO: 預計時間計算

    # 更新status
    gsutil.updateStatus(record[1], record[0], email_column - 1)  # email column還要改
