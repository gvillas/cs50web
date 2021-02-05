from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from . import util
from markdown2 import Markdown
from random import randint


class NewPage(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/404error.html")
    else:
        name = entry_name(entry)
        HTML_entry = util.get_entry(entry)
        markdowner = Markdown()
        HTML_entry = markdowner.convert(HTML_entry) 
        return render(request, "encyclopedia/entry.html",{
            "entry": HTML_entry,
            "name": name
        })


def search(request):
    entries = util.list_entries()
    query = request.GET.get('q', '')
    low_query = query.lower()
    low_entries = list()
    for entry in entries:
            low_entries.append(entry.lower())
    if low_query in low_entries:
        HTML_entry = util.get_entry(low_query)
        markdowner = Markdown()
        HTML_entry = markdowner.convert(HTML_entry) 
        return render(request, "encyclopedia/entry.html",{
            "entry": HTML_entry,
            "name": query.capitalize()
        }) 
    else:
        pages = list()
        for entry in low_entries:
            if low_query in entry:
                pages.append(entries[low_entries.index(entry)])
        if not pages:
            results = None
        else:
            pages.sort()
            results = pages
        return render(request, "encyclopedia/search.html", {
            "results": results,
            "query": query
        })


def add(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            entries = util.list_entries()
            low_entries = list()
            for entry in entries:
                low_entries.append(entry.lower())
            if title.lower() in low_entries:
                form = None
                return render(request, "encyclopedia/add.html", {
                    "form": form
                })
            content = form.cleaned_data["content"]
            util.save_entry(title=title, content=content)
            HTML_entry = util.get_entry(title)
            markdowner = Markdown()
            HTML_entry = markdowner.convert(HTML_entry)
            name = entry_name(title)
            return render(request, "encyclopedia/entry.html",{
                "entry": HTML_entry,
                "name": name
            })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewPage()   
    })
    

def edit(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title=title, content=content)
            HTML_entry = util.get_entry(title)
            markdowner = Markdown()
            HTML_entry = markdowner.convert(HTML_entry)
            name = entry_name(title)
            return render(request, "encyclopedia/entry.html",{
                "entry": HTML_entry,
                "name": name
            })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    title = request.GET.get('title', '')
    title = entry_name(title)
    entry = (util.get_entry(title)).replace('\r','')
    form = NewPage(initial={"title": title, "content": entry})
    return render(request, "encyclopedia/edit.html", {
        "form": form
    })


def random(request):
    entries = util.list_entries()
    number = randint(0, len(entries) - 1)
    entry = util.get_entry(entries[number])
    markdowner = Markdown()
    HTML_entry = markdowner.convert(entry)
    name = entry_name(entries[number])
    return render(request, "encyclopedia/entry.html",{
            "entry": HTML_entry,
            "name": name
        }) 


def entry_name(title):
    entries = util.list_entries()
    low_entries = list()
    for entry in entries:
            low_entries.append(entry.lower())
    return entries[low_entries.index(title.lower())]
    