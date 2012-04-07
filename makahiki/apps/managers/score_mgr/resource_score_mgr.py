"""The manager to manage resource score."""
from django.db.models.aggregates import Count
from django.db.models.expressions import F

from apps.managers.team_mgr.models import Team
from apps.widgets.energy_goal.models import TeamEnergyGoal
from apps.widgets.energy_scoreboard.models import EnergyData


def energy_ranks():
    """Get the overall ranking for all teams, return an ordered query set."""
    team_count = Team.objects.count()
    return EnergyData.objects.order_by("-date", "energy")[:team_count]


def energy_team_rank_info(team):
    """Get the overall rank for the team. Return a dict of the rank number and usage."""
    for idx, rank in enumerate(energy_ranks()):
        if rank.team == team:
            return {"rank": idx + 1, "usage": rank.energy}


def energy_goal_ranks():
    """Generate the scoreboard for energy goals."""
    # We could aggregate the energy goals in teams, but there's a bug in Django.
    # See https://code.djangoproject.com/ticket/13461
    return TeamEnergyGoal.objects.filter(
        actual_usage__lte=F("goal_usage")
    ).values(
        "team__name"
    ).annotate(completions=Count("team")).order_by("-completions")
