import os
import smtplib
import tldextract
from time import sleep
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from email.message import EmailMessage

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
}

def conect_mailbox(EMAIL_IMAP_SERVER, EMAIL_USER, EMAIL_PASS) -> MailBox:
	"""
    Tenta estabelecer a conexão IMAP com o provedor.
    Retorna o objeto MailBox logado ou None em caso de falha.
	"""
	print(f"🔌 Tentando conectar no servidor: {EMAIL_IMAP_SERVER}...")

	try:
		mailbox = MailBox(EMAIL_IMAP_SERVER).login(EMAIL_USER, EMAIL_PASS)
		print("✅ Conexão IMAP estabelecida com sucesso!\n")
		
		return mailbox
	except Exception as e:
		print(f"❌ Falha crítica ao conectar: {e}")
		print("Dica: Verifique seu .env e confirme se a Senha de App está correta.")
		return None

def format_remetente(folders_dict, remetente) -> str:
	if remetente in folders_dict.keys():
		remetente = folders_dict[remetente]

	return remetente

def move_email(mailbox, folders, msg, remetente) -> None:
	if remetente in folders:
		print(f"✅ A pasta '{remetente}' já existe.")
		mailbox.move(msg.uid, remetente)
	else:
		print(f'🆕 Criando a pasta: {remetente}\n')
		mailbox.folder.create(remetente)
		folders.append(remetente)
		sleep(1)
		mailbox.move(msg.uid, remetente)

def executar_processo() -> None:
	load_dotenv()

	# Configurações de Leitura (IMAP)
	EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER')
	EMAIL_USER = os.getenv('EMAIL_USER')
	EMAIL_PASS = os.getenv('EMAIL_PASS')

	mailbox = conect_mailbox(EMAIL_IMAP_SERVER, EMAIL_USER, EMAIL_PASS)

	if not mailbox:
		print('❌ Falha ao conectar no servidor.')
		return None

	try:
		# Buscar todos as pastas e salvar em um arquivo
		folders = [folder.name for folder in mailbox.folder.list()]
		PROVEDORES_PESSOAIS = ['gmail', 'hotmail', 'yahoo', 'outlook', 'icloud', 'live']
		all_emails = mailbox.uids()
		print(f"Total emails: {len(all_emails)}")

		print("📥 Buscando e-mails na Caixa de Entrada...")
		for msg in mailbox.fetch(reverse=True):
			print(f"Email: {msg.from_}")
			email = msg.from_values.email if msg.from_values else msg.from_

			if not email:
				continue

			empresa_provedor = tldextract.extract(email).domain

			remetente = email.split('@')[0].capitalize() if empresa_provedor in PROVEDORES_PESSOAIS else empresa_provedor.capitalize()

			remetente = format_remetente(folders_dict, remetente)
					
			move_email(mailbox, folders, msg, remetente)
			
			print("-" * 40)
	finally:
		print("🔌 Desconectando do servidor IMAP...")
		mailbox.logout()

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

if __name__ == "__main__":
	pass