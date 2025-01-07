import string
import requests
import random

def gen_code(value: int) -> list[str]:
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
    return list(codeSet)
