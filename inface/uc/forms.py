# coding: utf-8
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.models import ModelForm
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from inface.uc.models import *

class EmptyForm(forms.Form):
    confirm = forms.BooleanField(required=False)

class ChangeMyPasswordForm(forms.Form):
    """ change user password form """
    password = forms.CharField(
        label=_(u"Current password"),
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(),
    )
    password1 = forms.CharField(
        label=_(u"New password"),
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(),
    )
    password2 = forms.CharField(
        label=_(u"Confirmation"),
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(),
    )

    def clean_password(self):
        password = self.cleaned_data.get('password', None).strip()
        current_user = self.initial['current_user']
        if not current_user.check_password(password):
            raise forms.ValidationError(_(u'Current password is error'))
        return password

    def clean(self):
        cleaned_data = super(ChangeMyPasswordForm, self).clean()
        # ensures that any validation logic in parent classes is maintained.

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(_(u'The two passwords you typed do not match.'))

        return cleaned_data

class UserCreateForm(ModelForm):
    def clean(self):
        cleaned_data = super(UserCreateForm, self).clean()
        email = self.cleaned_data.get('email', None).strip()
        u = MyUser.objects.filter(email__iexact = email)
        if u.exists():
            raise forms.ValidationError(_(u'Email account is exist'))
        return cleaned_data
    class Meta:
        model = MyUser
        fields = ('email','first_name','last_name','dept','position','mobile','is_leader')

class UserResetPasswordForm(ModelForm):
    password = forms.CharField(
        label=_(u"Password"),
        min_length=6,
        max_length=18,
        widget=forms.PasswordInput(),
    )
    class Meta:
        model = MyUser
        fields = ('password',)

class UserUpdateForm(ModelForm):
    class Meta:
        model = MyUser
        fields = ('first_name','last_name','dept','position','mobile','is_active','is_admin','is_leader')

class DeptCreateForm(ModelForm):
    class Meta:
        model = Dept
        fields = ('name','parent')
class DeptUpdateForm(ModelForm):
    class Meta:
        model = Dept
        fields = ('name','parent', 'is_removed')
