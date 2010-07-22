import os

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from floors.models import Floor

def _get_available_themes():
  """Retrieves the available themes from the media folder."""
  
  theme_dir = os.path.join(settings.PROJECT_ROOT, "media")
  # Returns a list of tuples representing the name of the theme and the directory of the theme
  return ((item, item) for item in os.listdir(theme_dir) 
                      if os.path.isdir(os.path.join(theme_dir, item, "css")))
  
class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    name = models.CharField(_('name'), max_length=50, null=True, blank=True)
    about = models.TextField(_('about'), null=True, blank=True)
    points = models.IntegerField(default=0, editable=False)
    last_awarded = models.DateTimeField(null=True, blank=True, editable=False)
    theme = models.CharField(max_length=255, default="default", choices=_get_available_themes())
    floor = models.ForeignKey(Floor, null=True, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return ('profile_detail', None, {'username': self.user.username})
    get_absolute_url = models.permalink(get_absolute_url)
    
    def add_points(self, value, completion_date):
      """Adds points to the user and updates the last_awarded field."""
      self.points += value
      self.last_awarded = completion_date
      
    def remove_points(self, value, completion_date):
      """Removes points from the user.  
      If the completion date is the same as the last_awarded field, we rollback to a previously completed task."""
      
      from activities.models import CommitmentMember, ActivityMember, GoalMember
      
      self.points -= value
      if self.last_awarded == completion_date:
        self.last_awarded = self._last_completed_before(self, completion_date)
        
    def _last_completed_before(self, completion_date):
      """Time of the last task that was completed.  Returns None if there are no other tasks."""
      # Find the latest commitment/activity/goal that was completed.
      
      last_date = last_commitment = last_activity = last_goal = None
      try:
        last_commitment = CommitmentMember.objects.filter(
            user__pk=self.user,
            completion_date__isnull=False,
            completion_date__lte=completion_date,
        ).order_by("-completion_date")[0].completion_date
        last_date = last_commitment
      except IndexError:
        pass
        
      try:
        last_activity = ActivityMember.objects.filter(
            user=self.user,
            awarded__isnull=False,
            awarded__lte=completion_date,
        ).order_by("-awarded")[0].awarded
        if not last_date or last_date < last_activity:
          last_date = last_activity
      except IndexError:
        pass
      if self.floor:
        try:
          last_goal = GoalMember.objects.filter(
              floor=self.floor,
              awarded__isnull=False,
              awarded__lte=completion_date,
          ).order_by("-awarded")[0].awarded
          if not last_date or last_date < last_goal:
            last_date = last_goal
        except IndexError:
          pass
      
      return last_date
        
      
    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

def create_profile(sender, instance=None, **kwargs):
    if instance is None:
        return
    profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_profile, sender=User)
