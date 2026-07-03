import os
import smtplib
import tldextract
from time import sleep
from dotenv import load_dotenv
from imap_tools import MailBox, AND
from email.message import EmailMessage

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

def classificar_assunto(assunto: str, corpo_email) -> list:
	"""
		Classifica o assunto do e-mail em categorias predefinidas.
		Retorna a categoria correspondente ou 'Outros' se não houver correspondência.
	"""

	email = f'{assunto} {corpo_email}'.lower()

	# Melhorar a classificação de assuntos com palavras-chave específicas
	palavras_chave = {
		"Urgente": ["urgente", "asap", "prazo", "para ontem", "emergência"],
		"Financeiro": ["nota fiscal", "nf", "boleto", "fatura", "pagamento", "pix", "comprovante"],
		"Dúvida": ["como faz", "dúvida", "ajuda", "não consegui", "suporte"],
		"Vaga/Freela": ["proposta", "freelance", "oportunidade", "projeto"]
	}

	tags = []

	for categoria, palavras in palavras_chave.items():
		for palavra in palavras:
			if palavra in email:
				tags.append(categoria)
				break
	
	return tags if tags else ['Outros']

def create_email_body(remetente: str, destinatario: str, nome_cliente: str, assunto_original: str) -> EmailMessage:
	"""
    Cria e empacota um e-mail com fallback em Texto Plano e versão rica em HTML.
    Retorna o objeto EmailMessage pronto para ser disparado.
	"""
	msg = EmailMessage()

	# cabecalhos
	msg['Subject'] = f'RE: {subject}'
	msg['From'] = remetente
	msg['To'] = destinatario

	# fallback em Texto Plano
	texto_puro = f"""Olá {nome_cliente},

Recebemos o seu e-mail e nossa automação já está processando o seu pedido.
Responderemos em breve!

Um abraço,
Robô de Automação
"""
	
	msg.set_content(texto_puro)

	# versao HTML
	html = f"""
	<!DOCTYPE html>
    <html>
      <body style="font-family: Arial, sans-serif; color: #333333; line-height: 1.6;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eeeeee; border-radius: 8px;">
            <h2 style="color: #0070c9;">Olá, {nome_cliente}! 🚀</h2>
            <p>Recebemos o seu e-mail referente a <strong>"{assunto_original}"</strong>.</p>
            <p>Nossa automação já classificou a sua mensagem e ela está na fila de processamento.</p>
            <hr style="border: none; border-top: 1px solid #eeeeee; margin: 20px 0;">
            <p style="font-size: 12px; color: #777777;">
                Esta é uma mensagem automática gerada pelo sistema MailFlow. Por favor, não responda.
            </p>
        </div>
      </body>
    </html>
	"""

	msg.add_alternative(html, subtype='html')

	return msg

def send_email(
		EMAIL_SMTP_SERVER: str,
		EMAIL_SMTP_PORT: str,
		EMAIL_USER: str,
		EMAIL_PASS: str,
		body: EmailMessage
) -> bool:
	try:
		with smtplib.SMTP(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT) as smtp:
			smtp.starttls()
			smtp.login(EMAIL_USER, EMAIL_PASS)
			smtp.send_message(body)
			print("✅ E-mail enviado com sucesso!")
			return True
	except Exception as e:
		print(f"❌ Falha crítica ao enviar o e-mail: {e}")
		return False

def executar_processo() -> None:
	load_dotenv()

	# Configurações de Leitura (IMAP)
	EMAIL_IMAP_SERVER = os.getenv('EMAIL_IMAP_SERVER')
	EMAIL_USER = os.getenv('EMAIL_USER')
	EMAIL_PASS = os.getenv('EMAIL_PASS')
	EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER')
	EMAIL_SMTP_PORT = os.getenv('EMAIL_SMTP_PORT')
	SECURITY_SMTP = os.getenv('SECURITY_SMTP')

	mailbox = conect_mailbox(EMAIL_IMAP_SERVER, EMAIL_USER, EMAIL_PASS)

	if not mailbox:
		print('❌ Falha ao conectar no servidor.')
		return None

	try:
		emails = mailbox.fetch(reverse=True, mark_seen=True)

		for email in emails:
			corpot_email = email.text
			to_email = email.from_values.email if email.from_values.email else email.from_
			subject = email.subject

			tags = classificar_assunto(subject, corpot_email)

			print(f"📧 Novo e-mail de: {to_email}")
			print(f"Assunto: {subject}")
			print(f"🏷️  Categorias: {', '.join(tags)}")
			print('-' * 50)

			body_email = create_email_body(remetente=EMAIL_USER, destinatario=to_email, nome_cliente=to_email.split('@')[0].capitalize(), assunto_original=subject)
			send_email(EMAIL_SMTP_SERVER, EMAIL_SMTP_PORT, EMAIL_USER, EMAIL_PASS, body_email)

			break
	finally:
		print("🔌 Desconectando do servidor IMAP...")
		mailbox.logout()

if __name__ == "__main__":
	executar_processo()