import smtplib
from flask import current_app as app
from os import getenv, path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

def generate_message_html(assunto, receiver_email, html_message, cc=None, cco=None, pdf_attachment=[]):
    assunto = '[NÃO RESPONDA] BTA - {}'.format(assunto)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = getenv('MAILER_SENDER_EMAIL')
    msg['To'] = receiver_email
    if cc:
        msg['Cc'] = ','.join(cc)
    if cco:
        msg['Bcc'] = ','.join(cco)

    htmlPart = MIMEText(generate_default_email(html_message).encode('utf-8'), 'html', 'UTF-8')
    msg.attach(htmlPart)

    cpsPath = path.join(app.config['STATIC_FOLDER'], 'logos', 'logo-cps.png')
    fatecPath = path.join(app.config['STATIC_FOLDER'], 'logos', 'logo-fatec.png')
    
    with open(cpsPath, 'rb') as fpCps:
        imgCpsPart = MIMEImage(fpCps.read())
        imgCpsPart.add_header('Content-ID', '<{}>'.format('logo-cps.png'))
        msg.attach(imgCpsPart)

    with open(fatecPath, 'rb') as fpFatec:
        imgFatecPart = MIMEImage(fpFatec.read())
        imgFatecPart.add_header('Content-ID', '<{}>'.format('logo-fatec.png'))
        msg.attach(imgFatecPart)

    for item in pdf_attachment:
        with open(item[0], "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="pdf")
            attach.add_header('Content-Disposition','attachment', filename=str(item[1]))
            msg.attach(attach)

    return msg.as_string()

def generate_message_text(assunto, receiver_email, text_message):
    assunto = 'NÃO RESPONDA - {}'.format(assunto)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = getenv('MAILER_SENDER_EMAIL')
    msg['To'] = receiver_email
    textPart = MIMEText(text_message.encode('utf-8'), 'plain', 'UTF-8')
    msg.attach(textPart)
    return msg.as_string()

def send_email(receiver_email, message):
    smtp_server = getenv('MAILER_SMTP_SERVER')
    password = getenv('MAILER_PASSWORD')
    sender_email = getenv('MAILER_SENDER_EMAIL')

    with smtplib.SMTP(smtp_server, 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender_email, password)
        a = server.sendmail(sender_email, receiver_email, message)

def generate_default_email(inner_html):
    style = '''
        <style>
            *{
                color: black;
            }

            html{
                height: 100%;
            }

            body{
                font-family: sans-serif;
                margin: 0;
                padding: 0;
                position: relative;
                min-height: 100%;
            }

            .text-center{
                text-align: center;
            }

            .mt-10px{
                margin-top: 10px;
            }

            .w-80c{
                width: 80%;
                margin: 0px auto;
            }

            .w-100{
                width: 100%;
            }

            .w-75{
                font-size: 0.6rem;
                width: 75%;
            }

            .w-35{
                width: 35%;
            }

            .py-10px{
                padding-top: 10px;
                padding-bottom: 10px;
            }

            .padding-10{
                padding: 10px;
            }

            .mx-auto{
                margin-left: auto;
                margin-right: auto;
            }

            .font-2-rem{
                font-size: 2rem;
            }

            .font-15-rem{
                font-size: 1.5rem;
            }

            .bg-gray{
                background: lightgrey;
            }

            .aling-center{
                text-align: center;
            }

            .aling-justify{
                text-align: justify;
            }

            .d-block{
                display: inline-block;
            }

            footer{
                padding: 10px;
                background: #b3605d;
                position: relative;
                width: 100%;
                bottom: 0;
            }

            footer > p{
                color: white !important;
            }

            h2{
                text-align: center;
            }
        </style>
    '''
    msg = '''
    <html>
        <head>
            {0}
        </head>
        <body>
            <section class="py-10px w-100">
                <h2 class="text-center font-2-rem mt-10px">Sistema BTA - Biblioteca Virtual de Trabalhos Acadêmicos Prof. Me. Sílvio José Rosa</h2>
            </section>
            <section class="padding-10 w-80c">
                {1}
            </section>
            <section class="bg-gray py-10px w-100">
                <div class="w-75 mx-auto text-center">
                    <p>
                        Centro Paula Souza/Faculdade de Tecnologia de Carapicuíba: ISENÇÃO DE RESPONSABILIDADE: O conteúdo desta mensagem foi produzida eletronicamente através do sistema BTA, e enviado pelo usuário do sistema que o assina. 
                    </p>
                    <p>
                        O conteúdo foi adaptado para se adequar a pessoa que o recebe, e o texto final definido pelo próprio usuário do sistema que o assina. 
                    </p>
                    <p>
                        Caso discorde do conteúdo, ou este inclua informações ou palavras ofensivas que venham a prejudicá-lo, solicitamos que entre em contato imediatamente com o Diretor de sua Faculdade. 
                    </p>
                    <p>
                        As informações contidas nesta mensagem e seus arquivos anexos são destinadas exclusivamente ao endereço enviado, portanto, caso não seja o destinatário autorizado a recebê-la, solicitamos a gentileza de excluí-lo de sua caixa de entrada e em seguida reportar esta situação. 
                    </p>
                    <p>
                        Solicitamos a gentileza de manter sempre seu email atualizado no sistema de forma a receber as notificações de sua Faculdade, e que não marque esta caixa de remetente como lixo eletrônico, para não prejudicar futuras comunicações enviadas pelo sistema. 
                    </p>
                    <p>
                        NÃO RESPONDA: A caixa postal do remetente desta mensagem é do tipo não responda, que significa que nenhuma pessoa ou o próprio sistema irá ler a resposta caso esta seja enviada. 
                    </p>
                    <p>
                        Caso tenha interesse em responder, procure o canal adequado na própria Faculdade.
                    </p>
                </div>
            </section>
            <footer>
                <div class="aling-center">
                    <div class="mx-auto d-block">
                        <img src="cid:logo-cps.png" alt="">
                    </div>
                    <div class="mx-auto d-block">
                        <img src="cid:logo-fatec.png" alt="">
                    </div>
                </div>
                <p class="text-center mt-10px">Sistema de gerenciamento de usuários BTA.</p>
            </footer>
        </body>
    </html>
    '''.format(style, inner_html)
    return msg
