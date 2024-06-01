import smtplib
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, RECIPIENT_EMAIL

def send_email_notification(liquidation):
    company_name = liquidation['company_name']
    acn = liquidation['acn']
    date_published = liquidation['date_published']

    msg = MIMEText(f'Company: {company_name}\nNumber: {acn}\nDate: {date_published}')
    msg['Subject'] = 'New Company Liquidation Notice'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())