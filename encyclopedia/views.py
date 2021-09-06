from django.shortcuts import render

from . import util

import re

from random import choice



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry:
        context = {"entry":entry, "title":title}
        print(title)
        print(entry)
        return render(request, "encyclopedia/entry.html", context)

    else:
        return render(request, "encyclopedia/not_found.html")

def create_new_page(request):
    if request.POST:
        title = request.POST['title']
        if not util.get_entry(title):
            text = request.POST['content']
            util.save_entry(title, text)
            entry = util.get_entry(title)
            context = {"entry": entry, "title":title}
            return render(request, "encyclopedia/entry.html", context)
        else:
            context = {'title': title}
            return render(request, "encyclopedia/error.html", context)

    return render(request, "encyclopedia/new_page.html")

def edit_page(request, title):
    entry = util.get_entry(title)
    if entry:
        context = {"entry": entry, "title":title}
        if request.POST:
            title = request.POST['title']
            if util.get_entry(title):
                text = request.POST['content']
                util.save_entry(title, text)
                entry = util.get_entry(title)
                context = {"entry": entry, "title":title}
                return render(request, "encyclopedia/entry.html", context)
        return render(request, "encyclopedia/edit_page.html", context)
    else:
        return render(request, "encyclopedia/not_found.html")


def search_entries(request):
    title = request.GET['q']
    if title != '':
        entry = util.get_entry(title)
        if entry:
            context = {"entry":entry}
            return render(request, "encyclopedia/entry.html", context)
        else:
            search = re.compile(r'\w*{}\w*'.format(title), re.I)
            m_entry_list = []
            entry_list = util.list_entries()
            for entry in entry_list:
                match = search.search(entry)
                if match:
                    print(match)
                    m_entry_list.append(entry)
            if len(m_entry_list) > 0:
                return render(request, "encyclopedia/search.html", {
                "entries": m_entry_list
                })
            else:
                return render(request, 'encyclopedia/not_found.html')
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    



def rando_entry(request):
    entry_list = util.list_entries()
    title = choice(entry_list)
    entry = util.get_entry(title)
    context = {"entry":entry, 'title':title}
    return render(request, "encyclopedia/entry.html", context)
