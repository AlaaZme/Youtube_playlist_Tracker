import smtplib
from email.message import EmailMessage
import ssl
import yaml


def send_gmail(user_name, playlist):
    with open("config.yaml", "r") as f:
        config_data = yaml.safe_load(f)

    sender = config_data["gmail-sender"]
    password = config_data["gmail-sender-pass"]
    recv = config_data["gmail-receiver"]
    parent_dir = config_data['parent-dir']

    em = EmailMessage()
    try:
        textfile = f"{parent_dir}\\{user_name}\\_changeLog_{playlist}"
        with open(textfile, encoding="utf-8") as fp:
            if textfile:
                em.set_content(fp.read())
    except FileNotFoundError:
        em.set_content(f"New Playlist, {playlist}")

    em['From'] = sender
    em['To'] = recv
    em['Subject'] = f"update on: {user_name} , {playlist}"

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, recv, em.as_string())
