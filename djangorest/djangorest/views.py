from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

@login_required()
def home(request):
  context = {'some_key': 'some_value'}
  return render(request, 'home.html', context)