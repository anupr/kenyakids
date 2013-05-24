from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from web.views import gen_trans_db_strings_list
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

class Command(BaseCommand):
    can_import_settings = True

    def handle(self, *args, **kwargs):
        trans_group = get_object_or_404(Group, name="Translators")
        trans_users = User.objects.filter(groups=trans_group)

        email_content = ""
        for lang_code in settings.LANGUAGES:
            if not lang_code[0] == "en":
                untrans_strings = gen_trans_db_strings_list(lang_code[0])
                email_content += render_to_string("web/untrans_string_status.html",
                                                  {"untrans_strings": untrans_strings,
                                                   "lang_code": lang_code})

        recipients = filter(lambda x: x, trans_users.values_list('email', flat=True))
        send_mail(unicode(_("%(project_name)s Untranslated String Status" 
                            % {"project_name": settings.PROJECT_NAME})),
                  settings.DEFAULT_FROM_EMAIL,
                  recipients)
                                 
