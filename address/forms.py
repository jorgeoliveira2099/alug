from django import forms
from .models import Dados_usuario



class DadosUsuarioChangeForm(forms.DadosUsuarioChangeForm):
	class Meta(forms.DadosUsuarioChangeForm.Meta):
		model = Dados_usuario

class DadosUsuarioCreateForm(forms.DadosUsuarioCreateForm):
	class Meta(forms.DadosUsuarioCreateForm.Meta):
		model = Dados_usuario

