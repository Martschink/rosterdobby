# Create your views here.
from django.template import Context, loader
from django.http import HttpResponse
from dobby.models import Team, Player, Transaction
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import auth
#New for registration and authentication
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django import forms
import mechanize


from django.core.mail import send_mail

@login_required
def email_moves(request):
    message =""
    for team in Team.objects.all():
        message += team.name+"\n"
        for player in team.player_set.all():
            message += player.name +"  "+ player.date_added.strftime("%b %d, %Y ") + "\n"
        message += "\n"
    send_mail('Minor league rosters', message, "raulcastrorosterdobby@gmail.com",
    [request.user.email], fail_silently=False)
    return render_to_response("email.html", context_instance=RequestContext(request))
    

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/dobby/")



def index(request):
    teams = Team.objects.all()
    #return render_to_response('index.html', {'teams': teams})
    return render_to_response('index.html', {'teams': teams}, context_instance=RequestContext(request))

def transaction_log(request):
    transactions = Transaction.objects.all()
    return render_to_response('transactionlog.html', {'transactions': transactions}, context_instance=RequestContext(request))


def home(request):
    #return HttpResponse("Welcome to Roster Dobby!")
    teams = Team.objects.all()
    return render_to_response('index.html', {'teams': teams}, context_instance=RequestContext(request))


def team(request, team_id):
    team = Team.objects.get(id=team_id)
    return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))
    #return HttpResponse("You're looking transactions for team %s." % team_id)

@login_required
def eligibilityCheck(request, team_id):
    
    team = Team.objects.get(id=team_id)
    for player in team.player_set.all():
        player.IP = getIP(player.name)
        player.save()
            
    return render_to_response('eligibilityCheck.html', {'team': team}, context_instance=RequestContext(request))

def getIP(playername):
    #We can only search by last name.  Using the full name yields bad results.
    #So we'll split the player name if it includes a space, and then only use the second part of the name. We'll drop the case to lower case so we can use both names to confirm we found the right player.

	first = playername.split(" ")[0].lower()
	last = playername.split(" ")[-1].lower()

	mech=mechanize.Browser()
	URL="http://espn.go.com/mlb/players?search="
	page=mech.open(URL+last)

	u= page.geturl()
	print u
	if first in u and last in u:
		raw=page.read()
		if "WHIP" in raw and "ERA" in raw:
			IP = raw.split("Career")[-1].split("</td>")[5].split(">")[-1]
			return int(IP)




def player(request, player_id):
    if request.user.is_authenticated():
        return HttpResponse("You're unauthenticated and looking transactions for player %s." % player_id)
    else:
        return HttpResponse("You're authenticated and looking transactions for player %s." % player_id)

@login_required
def promote(request, team_id):
    team = Team.objects.get(id=team_id)
    #p = get_object_or_404(Team, pk=team_id)
    try:
        selected_player = team.player_set.get(pk=request.POST['player'])
        print selected_player
        #record the transaction to the log
        team.transaction_set.create(transaction_type="promoted", player_name=selected_player.name, transaction_date=timezone.now())
        team.save()

        selected_player.delete()
        #team.player_set.remove(selected_player)
        team.save()
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))
    except:
        return render_to_response('promote.html', {'team': team}, context_instance=RequestContext(request))
        #return render_to_response('promote.html', {'team': team})

    #return HttpResponse("You're looking transactions for team %s." % team_id)



@login_required
def add(request, team_id):
    team = Team.objects.get(id=team_id)

    try:
        player=request.POST['player']
        print player
        print team
        team.player_set.create(name=player, date_added=timezone.now())
        team.save()
        team.transaction_set.create(transaction_type="added", player_name=player, transaction_date=timezone.now())
        #transaction_event=Transaction(team, transaction_type="added", player_name=player, transaction_date=timezone.now())
        team.save()
        print "saved?"
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))
    except:
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))


@login_required
def demote(request, team_id):
    team = Team.objects.get(id=team_id)

    try:
        player=request.POST['player']
        print player
        print team
        team.player_set.create(name=player, date_added=timezone.now())
        team.save()
        team.transaction_set.create(transaction_type="demoted", player_name=player, transaction_date=timezone.now())
        team.save()
        print "saved?"
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))
    except:
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))




@login_required
def cut(request, team_id):
    team = Team.objects.get(id=team_id)
    #p = get_object_or_404(Team, pk=team_id)
    try:
        selected_player = team.player_set.get(pk=request.POST['player'])
        print selected_player
        #record the transaction to the log
        team.transaction_set.create(transaction_type="cut", player_name=selected_player.name, transaction_date=timezone.now())
        team.save()

        selected_player.delete()
        #team.player_set.remove(selected_player)
        team.save()
        return render_to_response('team.html', {'team': team}, context_instance=RequestContext(request))
    except:
        return render_to_response('cut.html', {'team': team}, context_instance=RequestContext(request))

