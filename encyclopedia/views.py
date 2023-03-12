from django.shortcuts import render
from django.http import HttpResponseNotFound
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry != None:
        entry_html =  markdown2.markdown(entry)
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "entry" : entry_html
        })
    else:
        return HttpResponseNotFound("The requested page was not found")