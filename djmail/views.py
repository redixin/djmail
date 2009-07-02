from util import rr
from mail.models import *
from django import forms

class DomainForm(forms.ModelForm):
    class Meta:
        model = Domain

@rr('mail/mail.html')
def index(request):
    return {}

@rr('mail/domains.html')
def domains(request):
    return { 'domains': Domain.objects.all() }

@rr('mail/domain_add.html')
def domain_add(request):
    return { 'form': DomainForm() }
