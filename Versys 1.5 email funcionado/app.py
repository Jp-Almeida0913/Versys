from flask import Flask, request, render_template, flash
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import zipfile
import logging

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'versystec369@gmail.com'
app.config['MAIL_PASSWORD'] = 'obzl llzr kuab rtyu'
app.config['MAIL_DEFAULT_SENDER'] = 'versystec369@gmail.com'

mail = Mail(app)

# Configurações para upload de arquivos
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'  # Adicionando uma chave secreta para flash messages

def allowed_file(filename):
    allowed_extensions = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

MAX_EMAIL_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_ATTACHMENT_SIZE = 25 * 1024 * 1024  # 25 MB

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == "POST":
        nome = request.form.get('nome')
        body = request.form.get('body')
        contato = request.form.get('contato')
        body = f"Contato do usuário: {contato}\n\n{body}"
        recipient = 'versysco@gmail.com'
        msg = Message(nome, recipients=[recipient])
        msg.body = body

        arquivos = request.files.getlist('arquivo')

        # Verifica o tamanho dos anexos
        for file in arquivos:
            if file and not allowed_file(file.filename):
                flash(f'Arquivo não permitido: {file.filename}', 'error')
                return render_template('feedback.html')

            if file and file.content_length > MAX_ATTACHMENT_SIZE:
                flash(f'Tamanho do anexo excede o limite de {MAX_ATTACHMENT_SIZE/(1024*1024)} MB: {file.filename}', 'error')
                return render_template('feedback.html')

        # Calcula o tamanho total do e-mail
        email_size = len(body.encode('utf-8'))
        for file in arquivos:
            if file:
                email_size += file.content_length

        if email_size > MAX_EMAIL_SIZE:
            flash(f'Tamanho total do e-mail excede o limite de {MAX_EMAIL_SIZE/(1024*1024)} MB.', 'error')
            return render_template('feedback.html')

        for file in arquivos:
            if file:
                nomearq = secure_filename(file.filename)
                if file.content_type == 'application/zip':
                    with zipfile.ZipFile(file.stream, 'r') as zip_ref:
                        for zip_info in zip_ref.infolist():
                            if zip_info.filename.endswith('/'):
                                flash(f'Pasta não permitida no arquivo ZIP: {zip_info.filename}', 'error')
                                return render_template('feedback.html')
                        msg.attach(nomearq, file.content_type, file.read())
                else:
                    msg.attach(nomearq, file.content_type, file.read())

        try:
            mail.send(msg)
            flash('Email enviado com sucesso!')
        except Exception as e:
            logging.error(f'Erro ao enviar email: {e}')
            flash(f'Erro ao enviar email: {e}')

    return render_template('feedback.html')

@app.route('/contact')
def contacts():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
