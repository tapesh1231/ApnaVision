from flask_mail import Message
from app import mail
from flask import current_app, render_template

def send_email(to, subject, template, **kwargs):
    msg = Message(
        subject,
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[to]
    )
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

def send_confirmation_email(user):
    token = user.generate_confirmation_token()
    send_email(
        user.email,
        'Confirm Your Account',
        'auth/email/confirm',
        user=user,
        token=token
    )
def send_reset_email(user):
    token = user.generate_reset_token()
    send_email(
        user.email,
        'Reset Your Password',
        'auth/email/reset_password',
        user=user,
        token=token
    )
