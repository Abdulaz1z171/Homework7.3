from django import forms
from django.core.validators import RegexValidator, MinLengthValidator

from app.models import Customer,User

class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ()


class LoginForm(forms.Form):
    # email = forms.EmailField()
    phone_number = forms.CharField(max_length=13)
    password = forms.CharField(max_length=255)

    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if not User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError('Bunday phone_number topilmadi')
        return phone_number

    def clean_password(self):
        phone_number = self.cleaned_data.get('phone_number')
        password = self.data.get('password')
        try:
            user = User.objects.get(phone_number=phone_number)
            if not user.check_password(password):
                raise forms.ValidationError('Parol xato')
        except User.DoesNotExist:
            raise forms.ValidationError(f'Bunday {phone_number} mavjud emas')
        return password

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone_number = self.cleaned_data.get('email')
    #     password = self.cleaned_data.get('password')
    #     user = User.objects.filter(email=email,password=password).first()
    #     if not user:
    #         raise forms.ValidationError('User topilmadi')
    #
    #     return cleaned_data


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    # email = forms.EmailField()
    phone_number = forms.CharField(max_length=13)
    password = forms.CharField(max_length=255)
    confirm_password = forms.CharField(max_length=255)



    def clean_phone_number(self):
        phone_number = self.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(f'Bunday {phone_number} allaqachon mavjud')
        return phone_number

    # def clean_email(self):
    #     email = self.data.get('email')
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError(f'Bunday {email} allaqachon mavjud')
    #     return email

    def clean_password(self):
        password = self.data.get('password')
        confirm_password = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password did not match')

        return password


    # def clean(self):
    #     cleaned_data = super().clean()
    #     password = self.data.get('password')
    #     confirm_password = self.data.get('confirm_password')
    #     if password != confirm_password:
    #         raise forms.ValidationError('Parollar mos tushmadi')
    #
    #     return cleaned_data