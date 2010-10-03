import settings
from registration import models
from django.core import mail
from django.template import loader, Context

def send_reg_confirmation(school):
    users = school.coaches.all()
    teams = school.team_set.all()
    messages = []
    for user in users:
        t = loader.get_template('mail/reg_confirmation.txt')
        c = Context({
            'user': user,
            'school': school,
            'teams': teams,
        })

        subject = settings.EMAIL_PREFIX + "Registration confirmation"
        body = t.render(c)
        emails = map(lambda u: u.email, users)
        message = mail.EmailMessage(subject=subject, body=body, to=emails, bcc=(settings.DEFAULT_FROM_EMAIL,))
        messages.append(message)

    connection = mail.get_connection()
    connection.send_messages(message)
