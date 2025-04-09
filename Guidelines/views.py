from django.shortcuts import render

# Create your views here.

def guidelines_cards(request):
    return render (request, 'guidelines/index.html',context= {})


def ai(request):
    return render (request, 'guidelines/ai_ml.html',context= {})


def data_analytics(request):
    return render (request, 'guidelines/data_analytics.html',context= {})

def data_engineer(request):
    return render (request, 'guidelines/data_engineering.html',context= {})


def research(request):
    return render (request, 'guidelines/academic_research.html',context= {})



