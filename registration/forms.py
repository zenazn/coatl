from django import forms
from django.forms import models as forms_models
from django.forms.models import modelformset_factory, inlineformset_factory
from django.forms.formsets import DELETION_FIELD_NAME
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import models

class RegisterUserForm(forms.Form):
    """
    Part one of the registration process: User registration

    Currently, there is not much protection against fake accounts. In the
    past this has not been an issue, so in the interest of streamlining the
    registration process any form of email verification has been omitted.
    """

    username = forms.CharField(max_length=30, min_length=3, label=_('Username'))
    first = forms.CharField(max_length=30, label=_('First Name'))
    last = forms.CharField(max_length=30, label=_('Last Name'))
    email1 = forms.EmailField(label=_('Email Address'))
    email2 = forms.EmailField(label=_('Confirm Email Address'))
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput())
    password2 = forms.CharField(label=_('Confirm Password'), widget=forms.PasswordInput())

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
            'first': self.cleaned_data.get('first'),
            'last': self.cleaned_data.get('last'),
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

class BaseMathleteFormSet(forms_models.BaseInlineFormSet):
    def clean(self):
        if hasattr(self, 'cleaned_data'):
            data = filter(bool, self.cleaned_data)
            #for mathletes in data:
                #if mathletes.round1 == mathletes.round2:
                  #raise forms.ValidationError, _("A Mathlete may not take the same test twice!")
            num_mathletes = len(data)
            if num_mathletes > 0 and (num_mathletes > 6 or num_mathletes < 4):
                pass
                #raise forms.ValidationError, _("Each team must have between 4 and 6 mathletes")

MathleteFormSet = inlineformset_factory(models.Team, models.Mathlete, formset=BaseMathleteFormSet, max_num=8, extra=8, fields=('first', 'last', 'alias', 'subject'))

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
            MathleteFormSet(data=self.data, instance=instance, prefix='MATHLETES-%s' % pk_value)
        ]

    def is_valid(self):
        result = super(BaseTeamFormSet, self).is_valid()

        for form in self.forms:
            if hasattr(form, 'nested'):
                for n in form.nested:
                    result = result and n.is_valid()

        return result

    def save_new(self, form, commit=True):
        instance = super(BaseTeamFormSet, self).save_new(form, commit=commit)
        form.instance = instance

        for nested in form.nested:
            nested.instance = instance
            for cd in nested.cleaned_data:
                cd[nested.fk.name] = instance
        return instance

    def should_delete(self, form):
        if self.can_delete:
            raw_delete_value = form._raw_value(DELETION_FIELD_NAME)
            should_delete = form.fields[DELETION_FIELD_NAME].clean(raw_delete_value)
            return should_delete
        return False

    def save_all(self, school, commit=True):
        objects = self.save(commit=False)

        if commit:
            for o in objects:
                if o:
                    o.school = school
                    o.save()
        else:
            self.save_m2m()

        for form in set(self.initial_forms + self.saved_forms):
            if not self.should_delete(form):
                for nested in form.nested:
                    n_objects = nested.save(commit=False)
                    for o in n_objects:
                        if o:
                            o.school = school
                            o.save()

TeamFormSet = inlineformset_factory(models.School, models.Team, formset=BaseTeamFormSet, max_num=3, extra=0, fields=('name', 'shortname', 'proctor', 'division'))

