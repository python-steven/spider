#-*-coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from django.core.mail  import  EmailMultiAlternatives, get_connection
from django.template import Context, loader
from django.conf import settings
from email.header import Header
import traceback
import os

# sender = 'Haojie_Ma@wistron.com'
# password = '1234mhjMHJ'
sender = 'wzs-tsc@wistron.com'
password = '1234qwer!@#$QWER'
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

def send_mail(receivers, subject, content, mail_type): 
    """ 按mail_type选定的格式发送邮件 """   
    ret = True
    try:
        msg = MIMEText(content, mail_type, 'utf-8')
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
    
def sendtextmail(receivers, content,subject):
    ret = True
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr(["AEMSLite System", sender])
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

def sendhtmlmail(receivers, subject, html_content):    
    ret = True
    try:
        msg = MIMEText(html_content, 'html', 'utf-8')
        msg['From'] = formataddr(["Devlop", sender])
        msg['To'] = formataddr(["Signers", ",".join(receivers)])
        msg['Subject'] = subject

        conn = smtplib.SMTP('wzs-tsc@wistron.com', 587) #wistron mail server, port 587
        conn.starttls()
        # conn.login(sender, password)
        conn.sendmail(sender, receivers, msg.as_string())
        conn.quit()

    except Exception as ex:
        traceback.print_exc()
        ret = False

    return ret

def get_html_content():
    # if action == 'form_approved':
    email_template_name = 'mail_template/form_approved.html'
    context = {'result': 'pass'}
    t = loader.get_template(email_template_name)
    html_content = t.render(context)
    return html_content

def send_approved_form_mail(to, subject, data):
    html_content = get_html_content()
    sendhtmlmail(to, subject, html_content)

def send_inform_pw_mail(to, subject, data):
    email_content = 'AEMS Lite System has automatically generated a new password for you.\r\n\r\n'
    email_content += "Your Account is: %s.\r\n" % data['user']
    email_content += "Your Password is: %s.\r\n" % data['pw']
    email_content += "\r\nPlease use your e-mail as user name and this password to login AEMSLite system."
    email_content += "After you login, please remember to change it. \r\n"

    email_content += "\r\n\r\nTHIS EMAIL WAS SENT BY PTS SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!\r\n"
    email_content += "AEMS Lite System http://10.41.95.106:90/index/"
    sendtextmail(to, email_content, subject)


def send_apply_form_mail(to, subject, data):   
    email_content = 'Dear %s, \n\n' % data['signer']
    email_content += "%s submit a budget code eform waiting for your review/approval.\r\n" % data['applicant']
    email_content += "You can click the below link to approve or reject. Thank you. \r\n"

    email_content += "\r\n\r\nTHIS EMAIL WAS SENT BY PTS SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!\r\n"
    email_content += "AEMS Lite System http://10.41.95.106:90/index/"
    sendtextmail(to, email_content, subject)

def send_user_forget_pwd_mail(to, data):
    """ 提交申请单后发送邮件给签核人签核 """
    subject = "Your password on AEMS Lite system has been changed"
    email_content = 'Dear %s, \n\n' % data['user_name']
    email_content += "Your password has been changed as below.\r\n"
    email_content += "%s \r\n" % data['new_pwd']
    email_content += "Please use %s and this password to login and remember to change it after you login successfully.\r\n" % data['employee_id']
    email_content += "\r\n\r\nTHIS EMAIL WAS SENT BY PTS SERVER AUTOMATICALLY. PLEASE DON'T DIRECTLY REPLY!!!\r\n"
    email_content += "AEMS Lite System http://10.41.95.89:90/index/"
    send_mail(to, subject, email_content, 'plain')

if __name__ == '__main__':
    email = 'vicily_wei@wistron.com'
    #mail = MailSender()
    # mail.send_approved_form_mail([email,], 'test', {'result': 'pass'})
    data = {'signer': "Vicily", 'employee_id': 'Z10041484', 'user_name': 'Vicily', 'new_pwd': '1234'}
    # send_inform_pw_mail([email,], 'test', data)
    send_user_forget_pwd_mail([email,], data)