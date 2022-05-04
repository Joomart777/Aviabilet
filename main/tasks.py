import time

from django.core.mail import send_mail

from main.celery import app


@app.task
def send_confirmation_email(code, email):
    time.sleep(3)
    full_link = f'http://localhost:8000/account/activate/{code}'
    send_mail(
        'Hello', # title
        full_link, # body
        'jasfargo@gmail.com', # from email
        [email] # to email
    )
