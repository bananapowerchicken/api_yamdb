from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from reviews.models import User

from api_yamdb.settings import DEFAULT_FROM_EMAIL

# YAMDB_MAIL = 'YaMDb@gmail.com'

def send_confirmation_code(user: User):
    confirmation_code = default_token_generator.make_token(user)

    send_mail(
            'YaMDb registration',
            f'Here is your confirmation code to use: {confirmation_code}',
            DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
