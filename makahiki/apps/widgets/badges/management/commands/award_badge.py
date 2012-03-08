"""award badge command"""

from django.core import management
from django.contrib.auth.models import User
import sys
from apps.lib.brabeion import badges


def award_badge(slug, username):
    """award the badge"""
    try:
        user = User.objects.get(username=username)
        badges.possibly_award_badge(slug, user=user)
    except User.DoesNotExist:
        sys.stderr.write("User with the username %s does not exist.\n" % username)
    except KeyError:
        sys.stderr.write("Badge with the slug %s does not exist.\n" % slug)


class Command(management.base.BaseCommand):
    """command"""
    help = 'Awards a badge (identified by its slug) to a user.'

    def handle(self, *args, **options):
        """
       Awards a badge (identified by its slug) to a user
        """
        if len(args) != 2:
            self.stderr.write("Usage: 'python manage.py award_badge <badge-slug> <user>\n")
            return

        slug = args[0]
        username = args[1]

        award_badge(slug, username)