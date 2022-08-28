from django import forms
from authentication.models import User

from .models import Team

class NewTeam(forms.ModelForm):
    team_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    Team_leader = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm", 'required': True}), required=False)
    member1 = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm"}), required=False)
    member2 = forms.EmailField(widget=forms.EmailInput(attrs={'class': "form-control form-sm"}), required=False)

    # def _init_(self, *args, **kwargs):
    #     super(NewTeam, self)._init_(*args, **kwargs)
    #     self.fields['event'].widget.attrs['class'] = 'form-control'
    #     self.fields['number_of_members'].widget.attrs['class'] = 'selecto form-control form-sm'
      
                
    class Meta:
        model = Team
        fields = ('event', 'team_name', 'number_of_members', 'Team_leader', 'member1', 'member2')