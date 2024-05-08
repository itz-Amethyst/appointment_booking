from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from djoser import utils

from core.models import VerificationCode


def fill_context_data(context, url, section):
    user = context.get("user")

    context["uid"] = utils.encode_uid(user.pk)
    context["token"] = default_token_generator.make_token(user)
    context["url"] = url

    verification_code , created = VerificationCode.objects.get_or_create(user = user, section = section)
    verification_code.token = context['token']
    verification_code.created_date = timezone.now()
    verification_code.section = section
    verification_code.is_active = True
    verification_code.save()
    return context