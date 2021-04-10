from django import forms
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class CreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
        required=True,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "username", "email",)
