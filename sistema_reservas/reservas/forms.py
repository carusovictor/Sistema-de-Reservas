from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import PerfilProfessor

class CadastroProfessorForm(UserCreationForm):
    nome_completo = forms.CharField(
        max_length=150,
        label="Nome Completo"
    )

    matricula = forms.CharField(
        max_length=20,
        label="Matrícula"
    )

    telefone = forms.CharField(
        max_length=20,
        label="Telefone"
    )

    class Meta:
        model = User
        fields = ["nome_completo", "matricula", "telefone", "password1", "password2"]

    def clean_matricula(self):
        matricula = self.cleaned_data["matricula"]

        if User.objects.filter(username=matricula).exists():
            raise forms.ValidationError("Já existe uma conta com essa matrícula.")
        
        return matricula
    
    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["matricula"]
        user.first_name = self.cleaned_data["nome_completo"]

        if commit:
            user.save()

            PerfilProfessor.objects.create(
                user=user,
                matricula=self.cleaned_data["matricula"],
                telefone=self.cleaned_data["telefone"]
            )

        return user