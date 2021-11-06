#from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.shortcuts import render
import bleach
from fixtures_website.get_fixtures import def_fixtures

from fixtures_website.apps.public import models
from fixtures_website.apps.public.models import Fixtures, Players

from .forms import SearchForm
from fixtures_website.helper import get_player_career, make_link

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            name = bleach.clean(form.cleaned_data['name'])
            link = make_link(name)

            if link == "None":
                return render(request, 'search.html', {'form': SearchForm(), 'fail' : 'Not Found'})
            else:
                player = get_player_career(link)
                return render(request, 'search.html', {'form': form, 'details' : player})

        else:
            form = SearchForm()

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SearchForm()

    return render(request, 'search.html', {'form': form})

def index(request):
    return render(request, 'index.html')

def leagues(request):
    return render(request, 'leagues.html')

def fixtures(request):
    def_fixtures()
    args = {}
    fixture_list = {}
    
    for i in Fixtures.objects.all():
        league = i.league
        fixtures = i.matches
        fixture_list[league] = fixtures
    args["fixtures"] = fixture_list
    return TemplateResponse(request, 'fixtures.html', args)

def LaLiga(request):
    return render(request, 'laliga.html')

def EPL(request):
    return render(request, 'EPL.html')

def Bundesliga(request):
    return render(request, 'BuLi.html')

def Ligue_1(request):
    return render(request, 'ligue1.html')

def Serie_A(request):
    return render(request, 'seriea.html')

def search(request):
    return render(request, 'search.html')

