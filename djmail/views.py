from djmail.models import *
from django.shortcuts import render_to_response
from django import forms

class EmailForm(forms.Form):
    email = forms.EmailField()
    old_password = forms.CharField(widget = forms.PasswordInput)
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)

def change_password(request):
    form = EmailForm()
    error = False
    from crypt import crypt
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            local_part, domain = request.POST['email'].split('@')
            try:
                user = User.objects.get(username = local_part, domain__name = domain)
                if user.crypt == crypt(request.POST['old_password'], user.crypt[:2]):
                    if request.POST['new_password'] == request.POST['new_password_1']:
                        user.password = request.POST['new_password']
                        user.save()
                        is_changed = True
            except User.DoesNotExist:
                error = True
    return render_to_response('main.html', {'form': form, 'error': error})
