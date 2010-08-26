from django import forms
from django.forms import models as forms_models
from django.forms.models import modelformset_factory, inlineformset_factory
from django.core import validators
from django.contrib.auth.models import User
from coatl.registration import models
from django.utils.translation import ugettext_lazy as _

class RegisterUserForm(forms.Form):
    """
    Part one of the registration process: User registration

    Currently, there is not much protection against fake accounts. In the
    past this has not been an issue, so in the interest of streamlining the
    registration process any form of email verification has been omitted.
    """

    username = forms.CharField(max_length=30, min_length=3, label=_('username'))
    email1 = forms.EmailField(label=_('email address'))
    email2 = forms.EmailField(label=_('confirm email address'))
    password1 = forms.CharField(label=_('password'), widget=forms.PasswordInput()) 
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput()) 

    def clean_username(self):
        try:
            User.objects.get(username=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError, _('That username is already taken')

    def clean_email2(self):
        if self.cleaned_data['email1'] != self.cleaned_data['email2']:
            raise forms.ValidationError(_('Emails must be the same'))
        return self.cleaned_data['email2']

    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(_('Passwords must be the same'))
        return self.cleaned_data['password2']
    
    def clean(self):
        return {
            'username': self.cleaned_data.get('username'),
            'email': self.cleaned_data.get('email1'),
            'password': self.cleaned_data.get('password1'),
        }


class RegisterSchoolForm(forms.ModelForm):
    """
    Part two of the registration process: School info
    """
    class Meta:
        model = models.School
        fields = ('name', 'address', 'school_type',)

MathleteFormSet = inlineformset_factory(models.Team, models.Mathlete, max_num=6, extra=6, can_delete=False, fields=('first', 'last', 'alias', 'round1', 'round2'))

class BaseTeamFormSet(forms_models.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(BaseTeamFormSet, self).add_fields(form, index)
        
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance = None
            pk_value = hash(form.prefix)

        form.nested = [
            MathleteFormSet(data=self.data, instance=instance, prefix='MATHLETES_%s' % pk_value)
        ]

TeamFormSet = inlineformset_factory(models.School, models.Team, formset=BaseTeamFormSet, max_num=3, can_delete=False, fields=('name', 'shortname', 'proctor', 'division'))

