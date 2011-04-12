# Create your views here.
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404

from components.quests.models import Quest, QuestMember

@login_required
def accept(request, quest_id):
  if request.method == "POST":
    referer = request.META["HTTP_REFERER"]
    quest = get_object_or_404(Quest, pk=quest_id)
    if quest.can_add_quest(request.user):
      member = QuestMember(user=request.user, quest=quest)
      member.save()

    return HttpResponseRedirect(referer)
  
  raise Http404
  
@login_required
def opt_out(request, quest_id):
  if request.method == "POST":
    referer = request.META["HTTP_REFERER"]
    quest = get_object_or_404(Quest, pk=quest_id)
    if quest.can_add_quest(request.user):
      member = QuestMember(user=request.user, quest=quest, opt_out=True)
      member.save()

    return HttpResponseRedirect(referer)
    
  raise Http404