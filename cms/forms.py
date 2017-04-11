from django.forms import ModelForm
from cms.models import Minutes


class MinutesForm(ModelForm):
    """Minutes form"""
    class Meta:
        model = Minutes
        fields = ('name', )
