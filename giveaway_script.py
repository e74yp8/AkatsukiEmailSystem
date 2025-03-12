import logging
from datetime import datetime

import requests
import email_util as eutil
from ticket_code_util import gen_code

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

email = "youisdoge@gmail.com"

value = 1

# gen ticket code
codeList = gen_code(value)

# 更新ticket db
idList = []
for code in codeList:
    rsp = requests.get(f"https://ticket-api.ketsuromoe.win/ticket/create/{code}/{email}")
    if rsp.status_code == 200:
        idList.append(int(rsp.text))

# 發送email
eutil.send_email(codeList, [600], email)
