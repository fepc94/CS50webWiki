from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
import markdown2


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
    search = request.GET.get("q")
    entries = util.list_entries()

    for entry in entries:
        if search.lower() == entry.lower():
            return redirect('entry', title=search)