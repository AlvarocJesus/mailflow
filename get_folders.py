import os
import smtplib
from email.message import EmailMessage
from imap_tools import MailBox, AND
from dotenv import load_dotenv
import tldextract
from time import sleep

load_dotenv()

# Configurações de Leitura (IMAP)
EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER')
PORT_IMAP_SERVER = os.getenv('PORT_IMAP_SERVER')
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS')
SECURITY_IMAP = os.getenv('SECURITY_IMAP')

# Configurações de Envio (SMTP)
EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')
SECURITY_SMTP = os.getenv('SECURITY_SMTP')

with MailBox(EMAIL_IMAP_SERVER).login(EMAIL_USER, EMAIL_PASS) as mailbox:
  print("🔍 Conectado. Lendo a estrutura atual de pastas...")

  # Buscar todos as pastas e salvar em um arquivo
  for folder in mailbox.folder.list():
    print(f"📁 Pasta: {folder.name}")