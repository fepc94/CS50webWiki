from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2
import re


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    '''    
    Returns an HTML page for the requested entry if it exists.
    Otherwise, an HTTP 404 Not Found error is returned. 
    ''' 
    entry = util.get_entry(title)
    if entry != None:
        entry_html =  markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "entry" : entry_html
        })
    else:
        return HttpResponseNotFound("The requested page was not found")

def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    matches = []

    for entry in entries: 
        if query.lower() == entry.lower():
            return redirect('entry', title=query)

        if re.search(query.lower(), entry.lower()):
            matches.append(entry)
            
    return render(request, "encyclopedia/search.html", {
            "query" : query,
            "matches" : matches
        })
