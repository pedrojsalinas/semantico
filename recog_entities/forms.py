from django import forms


class BuscadorForm(forms.Form):
    query = forms.CharField(label='Ingrese un texto', required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Qué estás buscando?'
        }))
