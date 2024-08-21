from flask import Flask, request, render_template, flash
from flask_mail import Mail, Message
import logging
import re
import dns.resolver


app = Flask(__name__)

# Configuração do Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'versystec369@gmail.com'
app.config['MAIL_PASSWORD'] = 'obzl llzr kuab rtyu'
app.config['MAIL_DEFAULT_SENDER'] = 'versystec369@gmail.com'

mail = Mail(app)

app.secret_key = 'supersecretkey'  # Chave secreta para flash messages

def is_valid_email_format(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def verify_email_domain(email):
    domain = email.split('@')[-1]
    try:
        dns.resolver.resolve(domain, 'MX')
        return True
    except dns.exception.DNSException:
        return False

def is_valid_email(email):
    return is_valid_email_format(email) and verify_email_domain(email)

@app.route('/sobre')
def sobre():
    return render_template('sobre.html')

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/projetos')
def projeto():
    return render_template('projetos.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        nome = request.form.get('nome')
        body = request.form.get('texto')
        email = request.form.get('email')

        if not is_valid_email(email):
            flash('O e-mail fornecido é inválido ou não existe.', 'error')
            return render_template('feedback.html')

        body = f"Contato do usuário: {email}\n\n{body}"
        recipient = 'versysco@gmail.com'

        if not is_valid_email(recipient):
            flash('E-mail do destinatário inválido.', 'error')
            return render_template('feedback.html')

        msg = Message(nome, recipients=[recipient])
        msg.body = body

        try:
            mail.send(msg)
            flash('Email enviado com sucesso!', 'success')
        except Exception as e:
            flash(f'Erro ao enviar email: {e}', 'error')

    return render_template('feedback.html')

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/manual')
def manual():
    return render_template("manual.html")

if __name__ == "__main__":
    app.run(debug=True)