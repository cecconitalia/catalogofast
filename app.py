from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os
import urllib.parse

app = Flask(__name__)

# Configurações do aplicativo Flask
app.secret_key = 'sua_chave_secreta'  # Substitua por uma chave secreta segura

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.seudominio.com'  # Substitua pelo servidor SMTP do seu provedor de e-mail
app.config['MAIL_PORT'] = 587  # Porta do servidor SMTP
app.config['MAIL_USE_TLS'] = True  # Ativar TLS
app.config['MAIL_USE_SSL'] = False  # Desativar SSL
app.config['MAIL_USERNAME'] = 'seu_email@seudominio.com'  # Substitua pelo seu e-mail
app.config['MAIL_PASSWORD'] = 'sua_senha'  # Substitua pela sua senha
app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@seudominio.com'  # E-mail remetente padrão

mail = Mail(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_email():
    # Obtém os dados do formulário
    name = request.form.get('name')
    email = request.form.get('email')
    whatsapp = request.form.get('whatsapp')
    message = request.form.get('message')

    # Cria a mensagem de e-mail
    msg = Message(
        subject="Novo Contato - Catálogo Fast",
        recipients=["catalogofast@outlook.com.br"],  # Substitua pelo e-mail desejado
        body=(
            f"Nome: {name}\n"
            f"Email: {email}\n"
            f"Whatsapp: {whatsapp}\n"
            f"Mensagem: {message}"
        )
    )

    try:
        mail.send(msg)
        flash("Mensagem enviada com sucesso!", "success")
    except Exception as e:
        flash("Erro ao enviar mensagem. Tente novamente mais tarde.", "danger")
        print(e)

    return redirect(url_for('home'))

@app.route('/send_whatsapp', methods=['POST'])
def send_whatsapp():
    # Obtém os dados do formulário
    name = request.form.get('name')
    email = request.form.get('email')
    whatsapp = request.form.get('whatsapp')
    message = request.form.get('message')

    # Cria a mensagem para o WhatsApp
    whatsapp_message = (
        f"Novo Contato - Catálogo Fast\n"
        f"Nome: {name}\n"
        f"Email: {email}\n"
        f"Whatsapp: {whatsapp}\n"
        f"Mensagem: {message}"
    )
    
    # Codifica a mensagem para ser usada na URL
    encoded_message = urllib.parse.quote(whatsapp_message)

    # Número do WhatsApp para onde será enviado
    phone_number = "5511968126748"  # Substitua pelo número desejado

    # Cria o link do WhatsApp
    whatsapp_link = f"https://wa.me/{phone_number}?text={encoded_message}"

    # Redireciona para o link do WhatsApp
    return redirect(whatsapp_link)

if __name__ == '__main__':
    app.run(debug=True)
app.config['MAIL_DEBUG'] = True
app.config['DEBUG'] = True
