from django import forms
from .models import UserBase
from django.contrib.auth.forms import (AuthenticationForm)

class UserLoginForm(AuthenticationForm):

        username = forms.CharField(widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Kullanici adi', 'id': 'login-username'}))
        password = forms.CharField(widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Şifre',
                'id': 'login-pwd',
            }
        ))
        
class UserEditForm(forms.ModelForm):

        email = forms.EmailField(
            label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
                attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

        first_name = forms.CharField(
            label='Firstname', min_length=4, max_length=50, widget=forms.TextInput(
                attrs={'class': 'form-control mb-3', 'placeholder': 'Firstname', 'id': 'form-firstname'}))

        class Meta:
            model = UserBase
            fields = ('email', 'first_name',)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].required = True
            self.fields['email'].required = True

          


class RegistrationForm(forms.ModelForm):
        """
        clean_<fieldname>()- yöntem, bir biçim alt sınıf çağrıldığında <fieldname>form alanı niteliğinin adı ile değiştirilir.
        Bu yöntem, o belirli özelliğe özgü, olduğu alanın türü ile ilgisi olmayan herhangi bir temizliği yapar.
        Bu yönteme herhangi bir parametre geçilmez.
        Alanın değerine bakmanız self.cleaned_datave bu noktada bunun formda gönderilen orijinal dize değil 
        bir Python nesnesi olacağını hatırlamanız gerekecek
        ( yukarıda cleaned_datagenel alan clean()yöntemi zaten temizlediği için olacaktır. verileri bir kez).
        """
        user_name = forms.CharField(label='Kullanici Adı', min_length=4, max_length=50, help_text='Required')
        email = forms.EmailField(max_length=100, help_text='Required',error_messages={'required': 'Lütfen bir email giriniz.'})
        password = forms.CharField(label='Şifre', widget=forms.PasswordInput)
        password2 = forms.CharField(label='Şifre Tekrar', widget=forms.PasswordInput)

        class Meta:
          model = UserBase
          fields = ('user_name','email',)
        
        def clean_username(self):
            user_name = self.cleaned_data['user_name'].lower()
            r = UserBase.objects.filter(user_name = user_name)
            if r.count():
              raise forms.ValidationError("Bu kullanici adina sahip bir kullanıcı zaten var.")
            return user_name

        def clean_password2(self):
            cd = self.cleaned_data
            if cd['password'] != cd['password2']:
              raise forms.ValidationError("Şifreler uyuşmuyor.")
            return cd['password2']

        def clean_email(self):
            m_email = self.cleaned_data['email']
            if UserBase.objects.filter(email=m_email).exists():
              raise forms.ValidationError("Bu email zaten kullanılmakta.")
            return m_email

      
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user_name'].widget.attrs.update({
              'class':'form-control mb-3','placeholder':'Kullanici adi'
            })
            self.fields['email'].widget.attrs.update({
              'class':'form-control mb-3','placeholder':'Email', 'name':'email'
            })
            self.fields['password'].widget.attrs.update({
              'class':'form-control mb-3','placeholder':'Şifre'
            })
            self.fields['password2'].widget.attrs.update({
              'class':'form-control mb-3','placeholder':'Şifre(Tekrar)'
            })


