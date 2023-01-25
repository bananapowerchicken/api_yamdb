from reviews.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

YAMDB_MAIL = 'YaMDb@gmail.com'

def send_confirmation_code(user: User):
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
            'YaMDb registration',
            f'Here is your confirmation code to use: {confirmation_code}',
            YAMDB_MAIL,
            [user.email],
            fail_silently=False,
        )
