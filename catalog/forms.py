import datetime 

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import BookInstance


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
    
    def clean_renewal_date(self):
        """
        Validator for renewal_date field. 
        """
        data = self.cleaned_data["renewal_date"]
        
        # Check if the date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in the past.'))
            
        # Check if a date is in the allowed range.
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead.'))
        
        # Remember to ALWAYS return the cleaned data
        return data

   
"""
# Equivalent using ModelForm instead of Form

class RenewBookModelForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']
        
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in the past.'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead.'))
        return data
    
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')}
"""     
    