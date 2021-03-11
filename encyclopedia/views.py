from django.shortcuts import render
import markdown
from . import util
from django import forms
import random

class Search_Form(forms.Form):
    search_query = forms.CharField()

class New_Page_Form(forms.Form):
    title = forms.CharField()
    textarea = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":15}))

class Edit_Form(forms.Form):
    etitle = forms.CharField()
    etextarea = forms.CharField(widget=forms.Textarea(attrs={"rows":2, "cols":15}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),"form":Search_Form
    })


#get entry content by its title
def Entry_page(request,title):
    entry_pages = util.get_entry(title)

    if entry_pages is None:
        content = "Requested page not found"
    
        return render(request,"encyclopedia/error.html",{
              "content":content ,"title":title
            })
    else:
        markcontent = util.get_entry(title)
        htmlcontent = markdown.markdown(markcontent)

        return render(request,"encyclopedia/title.html",{
              "content":htmlcontent ,"title":title,"form":Search_Form
            }) 

#search for specific entry
def search(request):
    if request.method == "POST":
        form = Search_Form(request.POST)
        if form.is_valid():
            query = form.cleaned_data["search_query"]
            entries = util.list_entries()
            for entry in entries:    # looping over each entry
                if query == entry:
                    markcontent = util.get_entry(query)
                    htmlcontent = markdown.markdown(markcontent)
                    return render(request,"encyclopedia/title.html",{"content":htmlcontent,"form":Search_Form,"title":query})
                    break
                result = [entry for entry in util.list_entries() if query in entry]
                if len(result) !=0:
                    return render(request,"encyclopedia/index.html",{"entries":result,"title":entry,"form":Search_Form})

def new_page(request):
    if request.method == "POST":
        form = New_Page_Form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["textarea"]
            entries = util.list_entries()
            for entry in entries:
                if title == entry:
                    return render(request,"encyclopedia/error.html",{"title":title,"content":"page already exists"})
                else:
                    save = util.save_entry(title,content)
                    markcontent = util.get_entry(title)
                    htmlcontent = markdown.markdown(markcontent)
                    search_form = Search_Form()
                    return render(request,"encyclopedia/title.html",{"title":title,"content":htmlcontent,"form":search_form})
    
    #this is for get request
    else:
        if request.method == "GET":
            form = Search_Form()
            newform = New_Page_Form()
            return render(request, "encyclopedia/newpage.html", {"form": form, "newform": newform})



def editpage(request,title):
    if request.method == "GET":
        default_entries = util.get_entry(title)
        editform = Edit_Form({"title":title,"etextarea":default_entries})
        return render(request,"encyclopedia/editpage.html",{"editform":editform})
    else:
        if request.method == "POST":
            eform= Edit_Form(request.POST)
            if eform.is_valid():
                etitle = eform.cleaned_data["etitle"]
                etextarea = eform.cleaned_data["etextarea"]
                save_entry = util.save_entry(etitle,etextarea)
                htmlcontent = markdown.markdown(etextarea)
                search = Search_Form()
                return render(request,"encyclopedia/title.html",{"title":etitle,"content":htmlcontent,"form":search})

def randoms(request):
    entries = util.list_entries()
    length = len(entries) - 1 

    entry = random.randint(0, length)
    title = entries[entry]
    markdowncontent = util.get_entry(title)
    htmlcontent = markdown.markdown(markdowncontent)
    form = Search_Form()
    return render(request, "encyclopedia/randompage.html", {"form": form, "title": title, "content": htmlcontent})














