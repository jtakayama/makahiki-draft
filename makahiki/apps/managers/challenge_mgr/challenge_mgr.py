"""The manager for challenge related settings."""

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import capfirst
from apps.managers.challenge_mgr.models import ChallengeSetting, RoundSetting, PageSetting, \
    PageInfo, GameInfo, GameSetting
from apps.utils import utils
from django.core import management


_game_admin_models = {}
"""private variable to store the registered models for game admin page."""


_site_admin_models = {}
"""private variable to store the registered models for site admin page."""


_sys_admin_models = {}
"""private variable to store the registered models for sys admin page."""


def init():
    """Initialize the challenge."""

    #if settings.DEBUG:
    #    import logging
    #    logger = logging.getLogger('django.db.backends')
    #    logger.setLevel(logging.DEBUG)
    #    logger.addHandler(logging.StreamHandler())

    #    logger = logging.getLogger('django_auth_ldap')
    #    logger.addHandler(logging.StreamHandler())
    #    logger.setLevel(logging.DEBUG)

    if settings.CHALLENGE.competition_name is not None:
        return

    # set the CHALLENGE setting from DB
    ChallengeSetting.set_settings()

    # get the Round settings from DB
    RoundSetting.set_settings()

    # create the admin
    create_admin_user()


def create_admin_user():
    """Create the admin user.
    Creates the admin user if it does not exist. Otherwise, reset the password to the ENV."""
    try:
        user = User.objects.get(username=settings.ADMIN_USER)
        if not user.check_password(settings.ADMIN_PASSWORD):
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()
    except ObjectDoesNotExist:
        user = User.objects.create_superuser(settings.ADMIN_USER, "", settings.ADMIN_PASSWORD)
        profile = user.get_profile()
        profile.setup_complete = True
        profile.setup_profile = True
        profile.completion_date = datetime.datetime.today()
        profile.save()


def info():
    """Returns the challenge name and site."""
    init()
    return "Challenge name : %s @ %s" % (settings.CHALLENGE.competition_name,
                                            settings.CHALLENGE.site_name)


def rounds_info():
    """Returns round info for this challenge."""
    init()

    info_str = ""
    rounds = get_all_round_info()
    for r in rounds.keys():
        info_str += r + " ["
        info_str += "start: %s" % rounds[r]["start"].date().isoformat()
        info_str += ", end: %s" % rounds[r]["end"].date().isoformat()
        info_str += "]"
    return info_str


def pages():
    """Returns a list of page names in this challenge."""
    return PageInfo.objects.all().values_list("name", flat=True)


def eval_page_unlock(user, page):
    """Returns True if the given page is unlocked based upon evaluation of its dependencies."""
    predicates = page.unlock_condition
    if not predicates:
        return False

    return utils.eval_predicates(predicates, user)


def all_page_info(user):
    """Returns a list of all pages with their current lock state."""
    all_pages = PageInfo.objects.exclude(name="home").order_by("priority")
    for page in all_pages:
        page.is_unlock = eval_page_unlock(user, page)
    return all_pages


def page_info(user, page_name):
    """Returns the specific page info object with its current lock state."""
    page = PageInfo.objects.filter(name=page_name)
    if page:
        page = page[0]
        page.is_unlock = eval_page_unlock(user, page)
        return page
    else:
        return None


def get_enabled_widgets(page_name=None):
    """Returns the enabled widgets for the specified page, taking into account of the PageSetting
    and GameSetting. if page_name is not specified, get all the enabled widgets from pageSetting
    and GameSetting."""

    widgets = []

    if page_name:
        page_setting = PageSetting.objects.filter(page__name=page_name, enabled=True)
    else:
        page_setting = PageSetting.objects.filter(enabled=True)

    for ps in page_setting:
        if ps.widget:
            widgets.append(ps.widget)
        if ps.game and GameInfo.objects.filter(name=ps.game, enabled=True).count():
            for gs in GameSetting.objects.filter(game=ps.game, enabled=True):
                widgets.append(gs.widget)

    return widgets


def register_page_widget(page_name, widget, label=None):
    """Register the page and widget."""
    if not label:
        label = page_name
    page, _ = PageInfo.objects.get_or_create(name=page_name, label=label)
    PageSetting.objects.get_or_create(page=page, widget=widget)


def available_widgets():
    """Returns a list of all the available widgets for the challenge."""
    return settings.INSTALLED_WIDGET_APPS


def get_all_round_info():
    """Returns a dictionary containing all the round information,
    example: {"Round 1": {"start": start_date, "end": end_date,}}"""
    return settings.COMPETITION_ROUNDS


def get_round_info(round_name=None):
    """Returns a dictionary containing round information, if round_name is not specified,
    returns the current round info. if competition end, return the last round.
    example: {"name": round_name, "start": start_date, "end": end_date,} """
    rounds = get_all_round_info()
    if not round_name:
        round_name = get_round_name()

    if round_name in rounds:
        return {"name": round_name,
                "start": rounds[round_name]['start'],
                "end": rounds[round_name]['end'],
                }
    else:
        return None


def get_round_name(submission_date=None):
    """Return the round name associated with the specified date, or else return None.
    if submission_date is not specified, return the current round name.
    if competition not started, return None,
    if competition end, return the last round."""
    rounds = get_all_round_info()
    if not submission_date:
        submission_date = datetime.datetime.today()

    if submission_date < settings.COMPETITION_START:
        return None

    # Find which round this belongs to.
    key = None
    for key in rounds:
        start = rounds[key]["start"]
        end = rounds[key]["end"]
        if submission_date >= start and submission_date < end:
            return key

    return key


def in_competition():
    """Return True if we are currently in the competition."""
    today = datetime.datetime.today()
    return settings.COMPETITION_START < today and today < settings.COMPETITION_END


def get_game_admin_models():
    """Returns the game related apps' info for admin purpose."""

    game_admins = ()
    for game in GameInfo.objects.all().order_by("priority"):
        game_admin = (game.name, game.enabled, game.pk,)
        for game_setting in game.gamesetting_set.all():
            widget = game_setting.widget
            if widget in _game_admin_models:
                game_admin += (_game_admin_models[widget],)
        game_admins += (game_admin,)
    return game_admins


def get_sys_admin_models():
    """return the sys admin models."""
    return get_admin_models(_sys_admin_models)


def get_site_admin_models():
    """return the site admin models."""
    return get_admin_models(_site_admin_models)


def get_admin_models(registry):
    """return the ordered tuple from the model registry."""
    models = ()
    for key in sorted(registry.keys()):
        models += ((key, registry[key]),)
    return models


def _get_model_admin_info(model):
    """return the admin info for the model."""
    return {"name": capfirst(model._meta.verbose_name_plural),
            "url": "%s/%s" % (model._meta.app_label, model._meta.module_name)}


def register_game_admin_model(widget, model):
    """Register the model of the game for admin purpose."""
    register_admin_model(_game_admin_models, widget, model)


def register_sys_admin_model(group, model):
    """Register the model for sys admin."""
    register_admin_model(_sys_admin_models, group, model)


def register_site_admin_model(group, model):
    """Register the model of site admin."""
    register_admin_model(_site_admin_models, group, model)


def register_admin_model(registry, group, model):
    """Register the model into a registry."""
    model_admin_info = _get_model_admin_info(model)
    if group in registry:
        registry[group] += (model_admin_info,)
    else:
        registry[group] = (model_admin_info,)

    registry[group] = sorted(registry[group])


class MakahikiBaseCommand(management.base.BaseCommand):
    """The base class for Makahiki command. Used when the init method of the
    challenge_mgr is called."""
    def __init__(self, *args, **kwargs):
        """Initialize the challenge_mgr."""
        init()
        super(MakahikiBaseCommand, self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        """Handle the command. Should be overridden by sub class."""
        pass
