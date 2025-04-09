from django.shortcuts import render
from django.http import HttpResponse

from About.models import TeamMembers
from About import forms

# Create your views here.

def about_us(request):
    team_list=TeamMembers.objects.order_by('first_Name')
    # Researchers_list=researcher_form.objects.get(pk=researcher_id)
    diction={'title':'Home Page','team_list':team_list}
    return render(request, "about_us/about.html", context=diction)



def team_info_form(request):
    new_form = forms.team_form_Details()

    if request.method == 'POST':
        new_form = forms.team_form_Details(request.POST, request.FILES)

        if new_form.is_valid():
            new_form.save(commit=True)
            return about_us(request)
        else:
            print('ERROR FORM INVALID', new_form.errors)
    dict1 = {'test_form': new_form, 'heading': 'Add New teammate'}

    return render(request, 'about_us/teaminfo_form.html', context=dict1)



def edit_team_info(request, member_id):
    members_info = TeamMembers.objects.get(pk=member_id)
    form = forms.team_form_Details(instance=members_info)
    diction = {}
    if request.method == "POST":
        form = forms.team_form_Details(request.POST, request.FILES, instance=members_info)

        if form.is_valid():
            form.save(commit=True)
            # return researcher_view(request)
            diction.update({'sucess_text': 'Successfully Updated '})


    diction.update({'edit_form': form})
    diction.update({'member_id': member_id})

    return render(request, 'about_us/edit_team.html', context=diction)


# Delete Research_Member

def delete_info(request,member_id):
    team_member= TeamMembers.objects.get(pk=member_id).delete()
    diction={'delete_text':'Successfully Deleted !'}
    return render(request,'about_us/delete.html',context=diction)
