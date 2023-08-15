from django import forms
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.forms import Form, ModelForm, DateField, widgets
from django.contrib.auth.forms import UserCreationForm
from account.models import Account
from . models import  Message
from ckeditor.widgets import CKEditorWidget
from django.contrib.auth import get_user_model

class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Message
        fields = ['sender','receiver', 'content','feedback']
        
        widgets =  {
            'sender'    : widgets.Select(attrs={'class': 'form-control'}),
            'receiver'  : widgets.Select(attrs={'class': 'form-control'}),
            'content'   : widgets.Textarea(attrs={'class': 'form-control', 'rows': 3 }),           
        }
    
    def __init__(self, *args, **kwargs):
            super(MessageForm,self).__init__(*args, **kwargs)
            self.fields['feedback'].required = False
            self.fields['content'].required = False
            # Set the default sender value
            self.fields['sender'].initial = get_user_model().objects.get(email='admin@jdvu.in')
