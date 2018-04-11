from django.shortcuts import render
from .forms import FormName
import pandas as pd
from .web_scrapper_new import Main
# Create your views here.

def index(request):
    return render(request,"search/index.html")

def newForm(request):
    form = FormName()
    data = []
    #"Author","profile_link","post_time","post_on","status","post_link"
    if request.method == "POST":
        form = FormName(request.POST)
        if form.is_valid():
            print("Validation Sucessfull!")
            print(form.cleaned_data["keyword"])
            df = Main(form.cleaned_data["keyword"])
            author = list(df.Author)
            profile_link = list(df.profile_link)
            post_time = list(df.post_time)
            post_on = list(df.post_on)
            status = list(df.status)
            post_link = list(df.post_link)
            for ind,val in enumerate(author):
                data.append({"author":val,"profile_link":profile_link[ind],"post_time":post_time[ind],"post_on":post_on[ind],"status":status[ind],"post_link":post_link[ind]})
            print("Data Scrapped!")

    # print(data)
    return render(request,"search/forms.html",{"form":form,"df":data})
    #"author":author,"profile_link":profile_link,"post_time":post_time,"post_on":post_on,"status":status,"post_link":post_link})
