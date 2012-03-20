from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import get_template
from templated_email import send_templated_mail

from odk_viewer.models import ParsedInstance
from utils.model_tools import queryset_iterator

class Command(BaseCommand):
    help = "Send an email to all formhub users"

    option_list = BaseCommand.option_list + (
        make_option("-m", "--message",
            dest="message",
            default=False,
        ),
    )

    def handle(self, *args, **kwargs):
        message = kwargs.get('message')
        verbosity = kwargs.get('verbosity')
        get_template('templated_email/notice.email')
        if not message:
            raise CommandError('message must be included in kwargs')
        # get all users
        #users = User.objects.all()
        # TODO uncomment above and remove below after testing
        users = User.objects.filter(pk__in=[7,91,159])
        for user in users:
            if verbosity:
                print 'Sending email to: %s' % user.email
            # send each email separately so users cannot see eachother
            send_templated_mail(
                template_name='notice',
                from_email='noreply@formhub.org',
                recipient_list=[user.email],
                context={
                    'username':user.username,
                    'full_name':user.get_full_name(),
                    'message': message
                },
            )
