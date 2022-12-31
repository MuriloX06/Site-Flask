from flask import Flask, render_template, redirect, request, flash
import smtplib
import email.message
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        fm = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        corpo_email = f"""
        <p>O {fm.nome} cujo o e-mail é {fm.email}, mandou uma mensagem: {fm.mensagem}</p>
        """

        msg = email.message.Message()
        msg['Subject'] = f"O {fm.nome} mandou mensagem do portfólio."
        msg['From'] = os.getenv("EMAIL")
        msg['To'] = 'muriloabreucastelobranco@gmail.com'
        password = os.getenv("SENHA")
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(corpo_email)

        s = smtplib.SMTP('smtp.gmail.com: 587')
        s.starttls()
        s.login(msg['From'], password)
        s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
        flash('Mensagem enviada com sucesso!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
