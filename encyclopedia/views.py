from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2, random
from . import util


def index(request):
    try: 
        query = request.GET["q"]
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("entry", kwargs={'title':request.GET["q"]}))

        return render(request, "encyclopedia/index.html", {
            "heading": "Search Results",
            "entries": list(filter(lambda s: query.upper() in s.upper(), util.list_entries()))
            })
    except:
        return render(request, "encyclopedia/index.html", {
            "heading": "All Pages",
            "entries": util.list_entries()
            })

def entry(request, title):
    markdwon = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "data": markdown2.markdown(markdwon) if markdwon else None,
        "title": title
    })

def new(request):
    if request.method == 'POST':
        if util.get_entry(request.POST.get('title')):
            return render(request, "encyclopedia/new.html", {"error": True})
        
        util.save_entry(request.POST.get('title'), request.POST.get('content'))
        return HttpResponseRedirect(reverse("entry", kwargs={'title':request.POST.get('title')}))

    return render(request, "encyclopedia/new.html")

def edit(request, title):
    return render(request, 'encyclopedia/edit.html', {
        "title": title,
        "content": util.get_entry(title)
    })

def confirm_edit(request):
    util.save_entry(request.POST.get('title'), request.POST.get('content'))
    return HttpResponseRedirect(reverse("entry", kwargs={'title':request.POST.get('title')}))

def random_entry(request):
    return HttpResponseRedirect(reverse("entry", kwargs={
        "title": random.choice(util.list_entries())
    }))