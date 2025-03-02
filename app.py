from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message
import os

print(os.urandom(24))  # Gera uma chave secreta de 24 bytes


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ofertacobrasilsc@gmail.com'        # Substitua pelo seu email
app.config['MAIL_PASSWORD'] = 'D8h5..12'                    # Substitua pela sua senha ou utilize variáveis de ambiente

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

    # Cria a mensagem de email
    msg = Message("Novo Contato - Catalogo Fast",
                  sender=email,
                  recipients=["ofertacobrasilsc@gmail.com"])
    msg.body = (
        f"Nome: {name}\n"
        f"Email: {email}\n"
        f"Whatsapp: {whatsapp}\n"
        f"Mensagem: {message}"
    )

    try:
        mail.send(msg)
        flash("Mensagem enviada com sucesso!", "success")
    except Exception as e:
        flash("Erro ao enviar mensagem. Tente novamente mais tarde.", "danger")
        print(e)

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

