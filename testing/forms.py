"""
Форма регистрации абитуриента перед тестированием.
"""
from django import forms
from .models import Abiturient


class AbiturientRegistrationForm(forms.ModelForm):

    class Meta:
        model = Abiturient
        fields = [
            'last_name', 'first_name', 'middle_name',
            'birth_date', 'school', 'grade', 'phone',
            'pin', 'birth_certificate',
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Иванов',
                'autocomplete': 'family-name',
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Иван',
                'autocomplete': 'given-name',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Иванович',
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date',
            }),
            'school': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Школа №1 г. Бишкек',
            }),
            'grade': forms.Select(attrs={
                'class': 'form-select',
            }),
            'pin': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '12345678901234',
                'maxlength': '14',
                'inputmode': 'numeric',
                'autocomplete': 'off',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+996 700 000000 или +7 900 000-00-00',
                'maxlength': '30',
                'type': 'tel',
                'autocomplete': 'tel',
            }),
            'birth_certificate': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'KPX 1234567',
                'maxlength': '30',
                'autocomplete': 'off',
                'style': 'text-transform:uppercase;letter-spacing:.04em',
            }),
        }
        labels = {
            'last_name': 'Фамилия',
            'first_name': 'Имя',
            'middle_name': 'Отчество',
            'birth_date': 'Дата рождения',
            'school': 'Школа / Учебное заведение',
            'grade': 'Оканчиваемый класс',
            'phone': 'Номер телефона',
            'pin': 'ПИН (14 цифр, из паспорта)',
            'birth_certificate': 'Свидетельство о рождении',
        }

    def clean_pin(self):
        pin = (self.cleaned_data.get('pin') or '').strip()
        if not pin:
            return None
        if not pin.isdigit():
            raise forms.ValidationError('ПИН должен содержать только цифры.')
        if len(pin) != 14:
            raise forms.ValidationError('ПИН должен содержать ровно 14 цифр.')
        if Abiturient.objects.filter(pin=pin).exists():
            raise forms.ValidationError(
                'Абитуриент с этим ПИН уже прошёл тестирование. '
                'Повторное прохождение недопустимо.'
            )
        return pin

    def clean_birth_certificate(self):
        bc = (self.cleaned_data.get('birth_certificate') or '').strip().upper()
        if not bc:
            return None
        if Abiturient.objects.filter(birth_certificate=bc).exists():
            raise forms.ValidationError(
                'Абитуриент с этим номером свидетельства уже прошёл тестирование.'
            )
        return bc

    def clean_last_name(self):
        return self.cleaned_data.get('last_name', '').strip().title()

    def clean_first_name(self):
        return self.cleaned_data.get('first_name', '').strip().title()

    def clean_middle_name(self):
        return self.cleaned_data.get('middle_name', '').strip().title()
