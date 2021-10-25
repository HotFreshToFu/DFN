from django import forms
from .models import Profile
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
import datetime


year = datetime.datetime.today().year  # 올해 년도

class ProfileForm(forms.ModelForm):
    name = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                # 'class': 'form-control',
                # 'placeholder': '이름을 입력하세요',
                'maxlength': 10,
            }
        )
    )
    WEX = forms.DateField(
        label='경력 시작일',
        widget=forms.SelectDateWidget(years=range(1980, year + 1))
        )
    DOB = forms.DateField(
        label='생년월일',
        widget=forms.SelectDateWidget(years=range(1980, year + 1))
        )
    level = forms.IntegerField(
        label='레벨',
        max_value = 3,
        min_value = 0
    )
    PTO = forms.IntegerField(label='사용한 연차 수', min_value = 0)
    team = forms.IntegerField(label='팀',min_value = 0)
    OFF = forms.IntegerField(label='OFF 수',min_value = 0)

    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ('user',)


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(
        label='이름',
        widget=forms.TextInput(
            attrs={
                # 'class': 'form-control',
                # 'placeholder': '이름을 입력하세요',
                'maxlength': 10,
            }
        )
    )
    WEX = forms.DateField(
        label='경력 시작일',
        widget=forms.SelectDateWidget(years=range(1980, year + 1))
        )
    DOB = forms.DateField(
        label='생년월일',
        widget=forms.SelectDateWidget(years=range(1980, year + 1))
        )
    level = forms.IntegerField(
        label='레벨',
        max_value = 3,
        min_value = 0
    )
    PTO = forms.IntegerField(label='사용한 연차 수', min_value = 0)
    team = forms.IntegerField(label='팀',min_value = 0)
    OFF = forms.IntegerField(label='OFF 수',min_value = 0)

    class Meta:
        model = Profile
        # fields = '__all__'
        exclude = ('user',)
        

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields