from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import User
from udyam_backend.models import Event
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from .models import Team, Workshop
from .forms import NewTeam
from .sheets import appendtosheet

from django.template.loader import get_template
from django.core.mail import EmailMessage

def LeaderBoard(request):
    return render(request, 'leaderboard.html')

@login_required
def Dashboard(request):
    user = User.objects.get(email=request.user)
    try:
        teams = Team.objects.filter(Team_leader=request.user) | Team.objects.filter(member1=request.user) | Team.objects.filter(member2=request.user)
    except:
        teams = None
    names_of_members = []
    if teams is not None:
        for team in teams:
            team_names = []
            leader = User.objects.get(email=team.Team_leader)
            if leader is not None:
                team_names.append(leader.first_name)

            try:
                member1 = User.objects.get(email=team.member1)
            except:
                member1 = None

            if member1 is not None:
                team_names.append(member1.first_name)

            try:
                member2 = User.objects.get(email=team.member2)
            except:
                member2 = None

            if member2 is not None:
                team_names.append(member2.first_name)
            names_of_members.append(team_names)

    TEAMS = zip(teams, names_of_members)

    if request.user.Year == '1':
        no_of_members = 3
    elif request.user.Year == '2' or request.user.Year == '3' or request.user.Year == '4':
        no_of_members = 2
    data = {
        'teams': TEAMS,
        'workshop': Workshop.objects.all()
    }

    if request.method == 'POST':
        form = NewTeam(request.POST)
        if form.is_valid():
            mail_subject = 'Confirmation of registration in ' +  form.cleaned_data.get('event').eventname + ' and WhatsApp group invitation.'
            try:
                ctx = {
                        'teamname': form.cleaned_data.get('team_name'),
                        'event': form.cleaned_data.get('event'),
                        'leader': User.objects.get(email=form.cleaned_data.get('Team_leader')).first_name
                }
            except:
                pass
            if isTeamNameTaken(form.cleaned_data.get('team_name'), form.cleaned_data.get('event')):
                return render(request, 'dashboard.html', {'data': data, 'form': form, 'teamnametaken': True})

            if form.cleaned_data.get('number_of_members') == '1':
                try:
                    team_leader = User.objects.get(email=form.cleaned_data.get('Team_leader'))
                    status = IsUserAlreadyRegister(team_leader, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderalready': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderemail': True})
                if request.user!=team_leader:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'notinteam': True})

                message = get_template('whatsapp_grp_invite.html').render(ctx)
                email = EmailMessage(mail_subject, message, to=[team_leader.email])
            elif form.cleaned_data.get('number_of_members') == '2':
                try:
                    team_leader = User.objects.get(email=form.cleaned_data.get('Team_leader'))
                    status = IsUserAlreadyRegister(team_leader, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderalready': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderemail': True})
                try:
                    member1 = User.objects.get(email=form.cleaned_data.get('member1'))
                    status = IsUserAlreadyRegister(member1, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'member1already': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'member1email': True})
                if team_leader==member1:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'teaminvalid': True})
                if request.user!=team_leader and request.user!=member1:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'notinteam': True})

                message = get_template('whatsapp_grp_invite.html').render(ctx)
                email = EmailMessage(mail_subject, message, to=[team_leader.email, member1.email])
            else:
                try:
                    team_leader = User.objects.get(email=form.cleaned_data.get('Team_leader'))
                    status = IsUserAlreadyRegister(team_leader, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderalready': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'leaderemail': True})
                try:
                    member1 = User.objects.get(email=form.cleaned_data.get('member1'))
                    status = IsUserAlreadyRegister(member1, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'member1already': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'member1email': True})
                try:
                    member2 = User.objects.get(email=form.cleaned_data.get('member2'))
                    status = IsUserAlreadyRegister(member2, form.cleaned_data.get('event'))
                    if status:
                        return render(request, 'dashboard.html', {'data': data, 'form': form, 'member2already': True})
                except ObjectDoesNotExist:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'member2email': True})
                if team_leader==member1 or member1==member2 or team_leader==member2:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'teaminvalid': True})
                if request.user!=team_leader and request.user!=member1 and request.user!=member2:
                    return render(request, 'dashboard.html', {'data': data, 'form': form, 'notinteam': True})

                message = get_template('whatsapp_grp_invite.html').render(ctx)
                email = EmailMessage(mail_subject, message, to=[team_leader.email, member1.email, member2.email])
            
            email.content_subtype = "html"
            email.send()
            form.save()
            try:
                team = Team.objects.get(team_name = ctx['teamname'], event = ctx['event'])
                sheetname = ctx['event'].eventname + " Teams"           
                appendtosheet(sheetname, team)
            except Exception as e:
                pass
            return HttpResponseRedirect('dashboard')
    else:
        form = NewTeam()
    return render(request, 'dashboard.html', {'data': data, 'form':form})


@login_required
def Team_delete(request, id):
    print("Delete")
    query = Team.objects.get(id=id)
    query.delete()
    return redirect('dashboard')

@login_required
def Update_User(request):
    if request.method == 'POST':
        currentUser = request.user
        currentUser.first_name = request.POST.get('username')
        currentUser.Phone = request.POST.get('contact')
        currentUser.save()
        return HttpResponseRedirect('dashboard')
    else:
        return HttpResponseRedirect('dashboard')

def IsUserAlreadyRegister(email, event):
    try:
        teams1 = Team.objects.filter(Team_leader=email)
    except:
        teams1 = None
    try:
        teams2 = Team.objects.filter(member1=email)
    except:
        teams2 = None
    try:
        teams3 = Team.objects.filter(member2=email)
    except:
        teams3 = None
    if teams1 is not None:
        for team in teams1:
            if team.event == event:
                return True
    if teams2 is not None:
        for team in teams2:
            if team.event == event:
                return True
    if teams3 is not None:
        for team in teams3:
            if team.event == event:
                return True
    return False

def isTeamNameTaken(name, event):
    try:
        teams = Team.objects.filter(team_name=name)
    except:
        teams = None
    if teams is not None:
        for team in teams:
            if team.event == event:
                return True
    return False

def teamView(request):
    return render(request, 'team.html')