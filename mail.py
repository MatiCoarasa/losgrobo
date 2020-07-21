import smtplib, ssl
from email.message import EmailMessage
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import get_current_time

mail = "robotinarmr@gmail.com"
password = "robotinarmr818"
port = 465
context = ssl.create_default_context()

path_csv = 'pedidos.csv'
path_template = 'template.html'

def send_mail(destinatarios, asunto, cuerpo=None, attachments=None):
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(mail, password)
        mensaje = armar_mensaje(mail, destinatarios, asunto, cuerpo, attachments)
        server.sendmail(mail, destinatarios, mensaje)


def armar_mensaje(mail, destinatarios, asunto, cuerpo_html, attachments):
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = ','.join(destinatarios)
    msg['Subject'] = asunto
    
    if cuerpo_html:
        msg.attach(MIMEText(cuerpo_html, 'html', 'utf-8'))

    for f in attachments or []:
        with open(f, 'rb') as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(f)
            )

        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    return msg.as_string().encode('ascii')


def read_destinatarios():
    destinatarios = ''
    with open('informe/destinatarios.txt') as f_dest:
        destinatarios = f_dest.read()
    
    return destinatarios.split(',')


def send_informe():
    destinatarios = read_destinatarios()
    asunto = f'Pedidos Grobobot - {get_current_time()}'

    send_mail(destinatarios=destinatarios, asunto=asunto, attachments=[path_csv])


def render_template():
    template = ''
    with open(path_template, 'r') as f_template:
        template = f_template.read()

    return template
