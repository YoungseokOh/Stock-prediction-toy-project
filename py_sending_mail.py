import smtplib, os, pickle  # smtplib: 메일 전송을 위한 패키지
import csv
from email import encoders  # 파일전송을 할 때 이미지나 문서 동영상 등의 파일을 문자열로 변환할 때 사용할 패키지
from email.mime.text import MIMEText   # 본문내용을 전송할 때 사용되는 모듈
from email.mime.multipart import MIMEMultipart   # 메시지를 보낼 때 메시지에 대한 모듈
from email.mime.base import MIMEBase     # 파일을 전송할 때 사용되는 모듈
import datetime

def sender(recipients):
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    #server.ehlo()
    #server.starttls()
    server.login('seok7302@gmail.com', 'dksrud129')
    now = datetime.datetime.now()
    print(now)
    nowDate = now.strftime('%m-%d')
    nowTime = now.strftime('%H:%M:%p')
    for item in recipients:
        body = """     
        """
        print('Sending... :' + item[1])
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '.'
        msg['From'] = 'bk_guys'
        msg['To'] = 'seok436@naver.com'
        msg.attach(MIMEText(body, 'html'))
        server.sendmail('bk_guys', 'seok7302@gmail.com', msg.as_string())
    print('Done!.')
    server.quit()