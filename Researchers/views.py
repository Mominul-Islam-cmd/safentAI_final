from django.shortcuts import render
from django.http import HttpResponse
from Researchers.models import researcher_form,researcher_recommend
from Researchers import forms

# Create your views here.
def info_form(request):
    new_form = forms.Researcher_form_Details()

    if request.method == 'POST':
        new_form = forms.Researcher_form_Details(request.POST, request.FILES)

        if new_form.is_valid():
            new_form.save(commit=True)
            return researcher_view(request)
        else:
            print('ERROR FORM INVALID', new_form.errors)
    dict1 = {'test_form': new_form, 'heading': 'Add New Researcher'}

    return render(request, 'Researchers/info_form.html', context=dict1)

# info_form show

def researcher_view(request):
    Researchers_list=researcher_form.objects.order_by('first_Name')
    # Researchers_list=researcher_form.objects.get(pk=researcher_id)
    diction={'title':'Home Page','Researchers_list':Researchers_list}
    return render(request, 'Researchers/info_show.html', context=diction)

# edit info_form


def edit_info(request, researcher_id):
    researchers_info = researcher_form.objects.get(pk=researcher_id)
    form = forms.Researcher_form_Details(instance=researchers_info)
    diction = {}
    if request.method == "POST":
        form = forms.Researcher_form_Details(request.POST, request.FILES, instance=researchers_info)

        if form.is_valid():
            form.save(commit=True)
            # return researcher_view(request)
            diction.update({'sucess_text': 'Successfully Updated '})
            

    diction.update({'edit_form': form})
    diction.update({'researcher_id': researcher_id})

    return render(request, 'Researchers/Edit_info.html', context=diction)


# Delete Research_Member

def delete_info(request,researcher_id):
    researchers_student= researcher_form.objects.get(pk=researcher_id).delete()
    diction={'delete_text':'Successfully Deleted !'}
    return render(request,'Researchers/delete.html',context=diction)




# research_recommend form
def recommend_form(request):
    new_form = forms.researcher_recommend_details()

    if request.method == 'POST':
        new_form = forms.researcher_recommend_details(request.POST)

        if new_form.is_valid():
            new_form.save(commit=True)
            return researcher_view(request)
       
    
    dict1 = {'test_form': new_form, 'heading': 'Add New Researcher'}

    return render(request, 'Researchers/Recommend_form.html', context=dict1)

# research_student_recommendation_show

# def research_student_recommendation_show(request):
#     Researchers_recommend = researcher_recommend.objects.order_by('id')
#     diction = {'title': 'Home Page', 'Researchers_recommend': Researchers_recommend}
#     return render(request, 'Researchers/recommend_details.html', context=diction)

def research_student_recommendation_show(request,researcher_id):
    researchers_info=researcher_form.objects.get(pk=researcher_id)
    researcher_recommend_details=researcher_recommend.objects.filter(researcher_id=researcher_id)
   
    dict={'researchers_info':researchers_info,'researcher_recommend_details':researcher_recommend_details}
    return render(request,'Researchers/recommend_details.html',context=dict)

