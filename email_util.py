import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
from string import Template
import qrcode
import os
import time_util
import logging

if not os.path.exists("img_temp"):
    os.mkdir("img_temp")  # 生成temp目錄


def send_email(codeSet: list[str], idList: list[int], email: str):
    content = MIMEMultipart()  # 建立MIMEMultipart物件
    content["subject"] = "測試郵件"  # 郵件標題 # TODO: 補一下郵件標題
    content["from"] = "fuyumatsuri2025.akatsuki@gmail.com"  # 寄件者
    content["to"] = email  # 收件者

    qrcodeCount = len(codeSet)

    # 預計入場時間計算
    time = time_util.time_cal(idList[0])

    qrcodeHTML = ""
    for i in range(qrcodeCount):
        qrcodeHTML += f"<h2>{idList[i]}</h2><img src='cid:img{i}'>\n"

    template = Template(Path("email_template.html").read_text(encoding="UTF-8"))
    body = template.substitute({"time": time, "qrcode": qrcodeHTML})

    content.attach(MIMEText(body, "html"))  # HTML郵件內容

    for i in range(qrcodeCount):
        code = codeSet[i]
        # 生成並儲存QR code
        img_path = f"img_temp\\qrcode_{code}.png"
        qrcode.make(code).save(img_path)

        # 讀取並附加QR code
        with open(img_path, 'rb') as fp:
            qrcode_file = MIMEImage(fp.read())

        os.remove(f"img_temp\\qrcode_{code}.png")  # 清除QR code

        qrcode_file.add_header('Content-ID', f'<img{i}>')  # 插入QR code
        content.attach(qrcode_file)

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("fuyumatsuri2025.akatsuki@gmail.com", "wrsbnwtoognlqpit")  # 登入寄件者gmail # TODO: smtp密碼
            smtp.send_message(content)  # 寄送郵件
            logging.info(f"{qrcodeCount}個qrcode已發送到{email}")
        except Exception as e:
            logging.error("email發送發生錯誤: %s", e)
