from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.templatetags.static import static
from django.http  import HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
import datetime as dt


# Create your views here.
def index(request):
    date = dt.date.today()
    return render(request,'index.html', {'date': date})