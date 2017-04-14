from django import forms
from django.forms import ModelForm
from django.forms import Form
from cms.models import Minutes


class MinutesForm(ModelForm):
    """Minutes form"""
    class Meta:
        model = Minutes
        fields = ('name', )
