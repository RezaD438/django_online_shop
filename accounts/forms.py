from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


class CustomCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username')


class CustomChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
