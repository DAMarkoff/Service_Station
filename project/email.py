from flask import render_template, url_for
from flask_mail import Message

from . import mail


def send_email(subject, recipients, text_body, html_body):
    msg = Message(subject, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)
    
    
def send_password_reset_email(user):
    token = user.get_reset_password_token()
    print(url_for('auth.reset_password', token=token, _external=True))
    send_email('[ServiceStation] Reset Your Password',
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))
    