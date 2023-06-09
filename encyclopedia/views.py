from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from . import util
from .forms import NewEntryForm
import markdown2
import re
import random


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
    '''
    Returns an HTML page for the searched entry if it exists.
    If the query matches any substring of an existing entry 
    (or entries) it returns a list of them. 
    '''
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

def newpage(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
     # create a form instance and populate it with data from the request:
        form = NewEntryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if util.get_entry(title) == None:
                util.save_to_disk(title, content)
                return redirect('entry', title=title)
            else:
                return HttpResponseNotFound("This entry already exists!") 

    else:
        form = NewEntryForm()

    return render(request, 'encyclopedia/newpage.html', {
        'form':form 
        })

def edit(request, title):
    # Retrieve the data from your storage mechanism based on the entry that needs to be edited.
    content = util.retrieve_entry(title)

    # Create a form instance and pass in the retrieved data as the initial data for the form.
    form = NewEntryForm(initial={'title': title, 'content': content})

    if request.method == 'POST':
        # If the request method is POST, validate the form data and update the entry in your storage mechanism.
        form = NewEntryForm(request.POST)
        if form.is_valid():
            updated_title = form.cleaned_data['title']
            updated_content = form.cleaned_data['content']
            util.update_entry(title, updated_title, updated_content)
            return redirect('entry', title=updated_title)

    # Render the form in your template with the initial data populated in the form fields.
    return render(request, 'encyclopedia/edit.html', {
        'title' : title,
        'form': form
        })

def randomize(request):
    """
    Renders a rondom entry via entry funcion.
    """
    title = lambda : random.choice(util.list_entries())
    return redirect('entry', title=title())