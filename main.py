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

folders_dict = {
  'Suajornadadedados': 'Jornada de Dados',
  'Adidas': 'Adidas',
  'Data Hackers': 'Data Hackers',
  'Datahackers': 'Data Hackers',
  'Dataquest': 'Data Hackers/Dataquest',
  'Diolinux': 'Diolinux',
  'Ebaconline': 'Ebaconline',
  'Empiricus': 'Empiricus',
  'Fei': 'Fei',
  'Filipedeschamps': 'Filipedeschamps',
  'Vintepila': 'Freelancer/Vintepila',
  'Workana': 'Freelancer/Workana',
  'Upwork': 'Freelancer/Upwork',
  'Github': 'Github',
  'Github Education': 'Github Education',
  'Githubeducation': 'Github Education',
  'Dependabot': 'dependabot',
  'Glassdoor': 'Glassdoor',
  'Membros': 'Membros',
  'Mercuriuscrypto': 'Mercurius Crypto',
  'Rundown': 'Rundown',
  'therundown': 'Rundown',
  'Therundown': 'Rundown',
  'Rundown AI': 'Rundown/Rundown AI',
  'Rundown Robotics': 'Rundown/Rundown Robotics',
  'Rundown Tech': 'Rundown/Rundown Tech',
  'Substack': 'Substack',
  'Suno': 'Suno',
  'Twitch': 'Twitch',
  'Xp': 'XP',
  'Xpi': 'XP',
  'Cursoemvideo': 'Curso em Vídeo',
  'Thedevelopersconference': 'The Dev Conf',
  'Dev': 'Dev to',
  'Balta': 'Balta io',
  'Beehiiv': 'Tech Drops',
  'Techdrops': 'Tech Drops',
  'Join1440': 'Daily Digest'
  # 'INBOX': 'INBOX',
  # '[Gmail]': '[Gmail]',
  # '[Gmail]/All Mail': '[Gmail]/All Mail',
  # '[Gmail]/Drafts': '[Gmail]/Drafts',
  # '[Gmail]/Important': '[Gmail]/Important',
  # '[Gmail]/Sent Mail': '[Gmail]/Sent Mail',
  # '[Gmail]/Spam': '[Gmail]/Spam',
  # '[Gmail]/Starred': '[Gmail]/Starred',
  # '[Gmail]/Trash': '[Gmail]/Trash',
}

with MailBox(EMAIL_IMAP_SERVER).login(EMAIL_USER, EMAIL_PASS) as mailbox:
  print("🔍 Conectado. Lendo a estrutura atual de pastas...")

  # Buscar todos as pastas e salvar em um arquivo
  folders = [folder.name for folder in mailbox.folder.list()]
  PROVEDORES_PESSOAIS = ['gmail', 'hotmail', 'yahoo', 'outlook', 'icloud', 'live']
  
  print("📥 Buscando e-mails na Caixa de Entrada...")
  # Buscar por todos os emails
  # for msg in mailbox.fetch(limit=100, reverse=True):
  for msg in mailbox.fetch(reverse=True):
    print(f"Email: {msg.from_}")
    email = msg.from_values.email if msg.from_values else msg.from_

    if not email:
      continue

    email_tld = tldextract.extract(email)
    empresa_provedor = email_tld.domain
    print(f'TLD Dominio: {empresa_provedor}')

    remetente = email.split('@')[0].capitalize() if empresa_provedor in PROVEDORES_PESSOAIS else empresa_provedor.capitalize()

    if remetente in folders_dict.keys():
      remetente = folders_dict[remetente]
        
    print(f"Processando: {msg.subject[:40]}...")
    print(f"De: {remetente}")

    if remetente in folders:
      print(f"✅ A pasta '{remetente}' já existe.")
      mailbox.move(msg.uid, remetente)
    else:
      print(f'🆕 Criando a pasta: {remetente}\n')
      mailbox.folder.create(remetente)
      folders.append(remetente)
      sleep(1)  # Aguardar 1 segundo para garantir que a pasta seja criada antes de mover o e-mail
      mailbox.move(msg.uid, remetente)
    
    print("-" * 40) # Só um separador visual pro seu terminal ficar bonito

    """
      print(msg.date, msg.subject, len(msg.text or msg.html))
      print({
        "date": msg.date,
        "subject": msg.subject,
        "flags": msg.flags,
        "from": msg.from_,
        "size": msg.size
      })
    """
