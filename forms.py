# coding=utf-8

from django.contrib.auth.models import User, Group
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
import uuid
from housing.models import USER_GROUP_RESIDENT, USER_GROUP_CONTRACTOR, UserProfile, UserAvatar

REGISTRATION_USER_GROUPS = (
    (0, USER_GROUP_RESIDENT),
    (1, USER_GROUP_CONTRACTOR),
)

class RegistrationForm(forms.Form):

    who_are_you = forms.ChoiceField(label=_(u'Who are you ?'), widget=forms.Select, choices=REGISTRATION_USER_GROUPS)
    first_name = forms.CharField(label=_(u'First Name'))
    last_name = forms.CharField(label=_(u'Last Name'))
    email = forms.EmailField(label=_(u'Email'))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_(u'Password'))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_(u'Password (again)'))

    def clean_email(self):

        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(
                _(u'This email address is already in use. Please supply a different email address.'))

        return self.cleaned_data['email']

    def clean(self):

        cleaned_data = super(RegistrationForm, self).clean()
        valid_two_pass = cleaned_data["password1"] != cleaned_data["password2"]

        if "password1" in cleaned_data and "password2" in cleaned_data and valid_two_pass:
            raise forms.ValidationError(u'The passwords are not the same')

        return cleaned_data

    def save(self):
        login = uuid.uuid4().hex[:30]

        email = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        user = User.objects.create_user(login, email, password)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # добавить юзера в выбранную группу
        print self.cleaned_data['who_are_you']
        print REGISTRATION_USER_GROUPS[int(self.cleaned_data['who_are_you'])]
        print REGISTRATION_USER_GROUPS[int(self.cleaned_data['who_are_you'])][0]
        print REGISTRATION_USER_GROUPS[int(self.cleaned_data['who_are_you'])][1]

        group = Group.objects.get(name=REGISTRATION_USER_GROUPS[int(self.cleaned_data['who_are_you'])][1])
        print group
        user.groups.add(group)

        # создать профайл
        profile = UserProfile()
        profile.user = user
        profile.save()
        # создать модель автарки
        #avatar = UserAvatar()
        #avatar.user = user
        #avatar.save()


        return user

class LoginForm(forms.Form):

    email = forms.EmailField(label=_('Email'))

    password = forms.CharField(widget=forms.PasswordInput, label=_("Password"))

    def clean(self):
        if 'email' in self.cleaned_data and 'password' in self.cleaned_data:
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            user = authenticate(username=email, password=password)

            if user is None:
                raise forms.ValidationError(_(u'Invalid login or password'))

        return self.cleaned_data

class ForgetPasswordForm(forms.Form):

    email = forms.EmailField(_(u'Email'))