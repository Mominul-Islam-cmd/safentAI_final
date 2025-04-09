from django.shortcuts import render
from django.http import HttpResponse
from PublicationProject.models import Publication,Project
from PublicationProject import forms
from django.shortcuts import redirect



# def publication(request):
#     if request.method == 'POST':
#         form = forms.Publication_form(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('publication')
        



def publication_form(request):
    new_form = forms.Publication_form()

    if request.method == 'POST':
        new_form = forms.Publication_form(request.POST, request.FILES)

        if new_form.is_valid():
            new_form.save(commit=True)
            return project_view(request)
        else:
            print('ERROR FORM INVALID', new_form.errors)

    dict1 = {'publication_form': new_form, 'heading': 'Add New Researcher'}

    return render(request, 'project_publication/publication_form.html', context=dict1)


# publication show

def publication_view(request):
    publication_iteams=Publication.objects.order_by('paper_title')
    # Researchers_list=researcher_form.objects.get(pk=researcher_id)
    project_iteams=Project.objects.order_by('project_title')
    diction={'title':'Home Page','publication_iteams':publication_iteams,'project_iteams':project_iteams}
    return render(request, 'project_publication/publication_show.html', context=diction)

 

# def publication_details(request):
#     publication_iteams=Publication.objects.order_by('paper_title')
#     # Researchers_list=researcher_form.objects.get(pk=researcher_id)
#     diction={'title':'Home Page','publication_iteams':publication_iteams}

#     return render(request, 'project_publication/publication_details.html', context=diction)


def edit_publication(request, id):
    paper_info = Publication.objects.get(pk=id)
    form = forms.Publication_form(instance=paper_info)
    diction = {}
    if request.method == "POST":
        form = forms.Publication_form(request.POST, request.FILES, instance=paper_info)

        if form.is_valid():
            form.save(commit=True)
            # return researcher_view(request)
            diction.update({'sucess_text': 'Successfully Updated '})
            

    diction.update({'edit_form': form})
    diction.update({'id': id})

    return render(request, 'project_publication/Edit_publication.html', context=diction)






# these code are projects



def project_form(request):
    new_form1 = forms.Project_form()

    if request.method == 'POST':
        new_form1 = forms.Project_form(request.POST, request.FILES)

        if new_form1.is_valid():
            new_form1.save(commit=True)
            return publication_view(request)
        else:
            print('ERROR FORM INVALID', new_form1.errors)

    dict1 = {'project_form': new_form1, 'heading': 'Add New project'}

    return render(request, 'project_publication/project_form.html', context=dict1)


# publication show

def project_view(request):
    project_iteams=Project.objects.order_by('project_title')
    # Researchers_list=researcher_form.objects.get(pk=researcher_id)
    diction={'title':'Home Page','project_iteams':project_iteams}
    return render(request, 'project_publication/publication_show.html', context=diction)

# def publication_details(request):
#     publication_iteams=Publication.objects.order_by('paper_title')
#     # Researchers_list=researcher_form.objects.get(pk=researcher_id)
#     diction={'title':'Home Page','publication_iteams':publication_iteams}

#     return render(request, 'project_publication/publication_details.html', context=diction)


def edit_project(request, id):
    project_info = Project.objects.get(pk=id)
    form = forms.Project_form(instance=project_info)
    diction = {}
    if request.method == "POST":
        form = forms.Project_form(request.POST, request.FILES, instance=project_info)

        if form.is_valid():
            form.save(commit=True)
            # return researcher_view(request)
            diction.update({'sucess_text': 'Successfully Updated '})
            

    diction.update({'edit_form': form})
    diction.update({'id': id})

    return render(request, 'project_publication/Edit_project.html', context=diction)
