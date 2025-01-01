from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from pathlib import Path
import smtplib
from string import Template
import qrcode
import os


def send_email(codeSet: list[str], idList: list[int], time: str, email: str):
    content = MIMEMultipart()  # 建立MIMEMultipart物件
    content["subject"] = "This is a subject"  # 郵件標題 #TODO: 補一下郵件標題
    content["from"] = "williamhon404@gmail.com"  # 寄件者 #TODO: 改寄件者
    content["to"] = email  # 收件者

    qrcodeCount = len(codeSet)

    qrcodeHTML = ""
    for i in range(qrcodeCount):
        qrcodeHTML += f"<h2>{idList[i]}</h2><img src='cid:img{i}'>\n"

    template = Template(Path("email_template.html").read_text(encoding="UTF-8"))
    body = template.substitute({"time": time, "qrcode": qrcodeHTML})

    content.attach(MIMEText(body, "html"))  # HTML郵件內容

    if not os.path.exists("EmailBackend/img_temp"):  # 生成temp目錄
        os.mkdir("EmailBackend/img_temp")

    for i in range(qrcodeCount):
        code = codeSet[i]
        qrcode.make(code).save(f"img_temp\\qrcode_{code}.png")  # 生成並儲存QR code
        fp = open(f"img_temp\\qrcode_{code}.png", 'rb')
        qrcode_file = MIMEImage(fp.read())

        fp.close()

        os.remove(f"img_temp\\qrcode_{code}.png")  # 清除QR code

        qrcode_file.add_header('Content-ID', f'<img{i}>')  # 插入QR code
        content.attach(qrcode_file)

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("williamhon404@gmail.com", "")  # 登入寄件者gmail #TODO: smtp密碼
            smtp.send_message(content)  # 寄送郵件
            print(f"{qrcodeCount}個qrcode已發送到{email}！")  # TODO: (全部)優化loging
        except Exception as e:
            print("email發送發生錯誤: ", e)
