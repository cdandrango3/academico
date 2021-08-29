from django.forms import ModelForm
from django import forms
from djangoProject.clase.models import notas
from djangoProject.clase.models import notas as calificacion
class Nota(ModelForm):

    class Meta:
        model = notas
        fields = ['nota']
        widgets = {
            'nota': forms.NumberInput(
                attrs = {
                'class':'m-4',
                'placeholder': 'ingrese la nota'
        }
        )
        }
    def clean_nota(self):
        notas=self.cleaned_data['nota']
        if notas>20 or notas<0:
            raise forms.ValidationError("la nota deber ser del 0 al 20")
        return notas




'''
 def save(self,commit=True):
        m=super().save(commit=False)
        m.nota=self.cleaned_data.get('nota')
        if commit:
            m.save()
            return m
'''