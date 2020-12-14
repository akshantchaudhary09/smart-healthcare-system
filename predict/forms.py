from django.forms import ModelForm
from .models import Report

class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['name', 'age', 'gender', 'height', 'weight', 'symptom1', 'symptom2',
                  'symptom3','symptom4','symptom5', 'disease', 'consultDoctor']
