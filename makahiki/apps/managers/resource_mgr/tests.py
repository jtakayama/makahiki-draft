"""Energy scoreboard Test"""
import datetime

from django.test import TransactionTestCase
from django.contrib.auth.models import User
from apps.managers.resource_mgr import resource_mgr
from apps.managers.resource_mgr.models import EnergyUsage
from apps.managers.team_mgr.models import Team


class ResourceManagerTestCase(TransactionTestCase):
    """ResourceManager Test"""
    fixtures = ["base_teams.json"]

    def setUp(self):
        """Initialize a user and log them in."""
        self.user = User.objects.create_user("user", "user@test.com", password="changeme")
        self.team = Team.objects.all()[0]

    def testEnergy(self):
        """test Energy."""
        date = datetime.date.today()
        _ = EnergyUsage.objects.create(
            team=self.team,
            date=date,
            time=datetime.time(hour=15),
            usage=100,
        )

        rank = resource_mgr.energy_team_rank_info(self.team)["rank"]
        usage = resource_mgr.team_energy_data(date=date, team=self.team).usage
        self.assertEqual(rank, 1, "The team should be first rank.")
        self.assertEqual(usage, 100, "The team usage.is not correct.")