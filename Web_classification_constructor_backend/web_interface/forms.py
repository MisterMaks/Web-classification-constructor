from django import forms


class Form1(forms.Form):
    field_1 = forms.IntegerField(required=False, help_text=" - Число")
    field_2 = forms.CharField(required=False, initial="", help_text=" - Текст")
    choices = [(1, 1), (2, 2), (3, 3)]
    field_3 = forms.ChoiceField(choices=choices, required=False, initial="", help_text=" - Выбор")
