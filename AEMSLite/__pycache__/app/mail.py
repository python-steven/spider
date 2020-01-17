import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import traceback
# sender = 'Haojie_Ma@wistron.com'
# password = '1234mhjMHJ'
sender = 'Steven_X_Xu@wistron.com'
password = 'Wistron123'
def sendmail(receivers, content,subject):
    ret = True
    try:
        msg = MIMEText(content, 'html', 'utf-8')
        msg['From'] = formataddr(["Devlop", sender])
        msg['To'] = formataddr(["Signers", ",".join(receivers)])
        msg['Subject'] = subject

        conn = smtplib.SMTP('wzsowa.wistron.com', 587) #wistron mail server, port 587
        conn.starttls()
        conn.login(sender, password)
        conn.sendmail(sender, receivers, msg.as_string())
        conn.quit()

    except Exception as ex:
        traceback.print_exc()
        ret = False

    return ret

