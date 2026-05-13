from django import forms


class ContactForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "id": "exampleInputEmail1"}
        ),
        error_messages={
            "required": "Podaj swój adres Email",
            "invalid": "Podaj poprawny adres Email",
        },
    )

    title = forms.CharField(
        label="Tytuł",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "exampleInputPassword1"}
        ),
        error_messages={
            "required": "Podaj tytuł wiadomości",
            "max_length": "Tytuł nie może być dłuższy niż 100 znaków",
        },
    )

    message = forms.CharField(
        label="Treść wiadomości",
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "id": "floatingTextarea2",
                "style": "height: 100px",
            }
        ),
        error_messages={"required": "Podaj treść wiadomości"},
    )
