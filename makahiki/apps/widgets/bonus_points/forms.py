"""Form for validating Bonus Points."""

'''
Created on Aug 5, 2012

@author: Cam Moore
'''

from django import forms


class BonusPointsForm(forms.Form):
    """bonus points form in the Bonus Points widget."""
    response = forms.CharField(widget=forms.TextInput(attrs={'size': '12'}))